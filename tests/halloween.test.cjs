// Dependency-free date/lifecycle checks: node --test tests/halloween.test.cjs
const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../assets/halloween.js'), 'utf8');

function harness(instant, {ready = true, quiet = false, storageBlocked = false} = {}) {
  let now = instant;
  const classes = new Set(), nodes = [], events = {}, timers = new Map();
  const storage = new Map([['aevum-halloween-quiet', String(quiet)]]);
  const list = {toggle(key, state) {if (state) classes.add(key); else classes.delete(key);}, remove(key) {classes.delete(key);}};
  const button = {attrs: {}, setAttribute(k, v) {this.attrs[k] = v;}, addEventListener(_, fn) {this.click = fn;}};
  const body = {append(el) {nodes.push(el);}, prepend(el) {nodes.push(el);}};
  const document = {
    documentElement: {classList: list}, body: ready ? body : null,
    readyState: ready ? 'complete' : 'loading',
    createElement() {return {attrs: {}, setAttribute(k, v) {this.attrs[k] = v;}, querySelector() {return button;}, remove() {nodes.splice(nodes.indexOf(this), 1);}};},
    querySelector() {return {after(el) {nodes.push(el);}};},
    addEventListener(name, fn) {events[name] = fn;}
  };
  vm.runInNewContext(source, {
    document, Intl, Date: class extends Date {constructor() {super(now);}},
    sessionStorage: {getItem(k) {if(storageBlocked) throw Error('disabled'); return storage.get(k);}, setItem(k,v) {if(storageBlocked) throw Error('disabled'); storage.set(k,v);}},
    window: {addEventListener(name, fn) {events[name] = fn;}},
    setInterval(fn) {timers.set(1,fn); return 1;}, clearInterval(id) {timers.delete(id);}
  });
  return {classes, nodes, events, timers, button, storage, setTime(value) {now=value;}, load() {document.body=body; events.DOMContentLoaded();}};
}

test('only October 30–31, 2026 in Berlin, independent of visitor timezone', () => {
  for(const [date, active] of [
    ['2026-10-29T22:59:59Z', false], ['2026-10-29T23:00:00Z', true],
    ['2026-10-30T23:00:00Z', true], ['2026-10-31T22:59:59Z', true],
    ['2026-10-31T23:00:00Z', false], ['2027-10-30T12:00:00Z', false]
  ]) {
    const h=harness(date);
    assert.equal(h.classes.has('halloween-night'), active, date);
    assert.equal(h.nodes.length, active ? 2 : 0, date);
    assert.equal(h.timers.size, active ? 1 : 0, date);
  }
});
test('head script sets the costume class, waits for body, mounts exactly once', () => {
  const h=harness('2026-10-30T12:00:00Z', {ready:false});
  assert(h.classes.has('halloween-night')); assert.equal(h.nodes.length,0);
  h.load(); h.events.pageshow(); assert.equal(h.nodes.length,2);
});
test('an open tab returns to its original design after Berlin midnight', () => {
  const h=harness('2026-10-31T22:59:58Z', {quiet:true});
  h.setTime('2026-10-31T23:00:00Z'); [...h.timers.values()][0]();
  assert.equal(h.nodes.length,0); assert.equal(h.classes.size,0); assert.equal(h.timers.size,0);
});
test('resuming a suspended tab expires the costume without waiting for its timer', () => {
  const h=harness('2026-10-31T21:00:00Z');
  h.setTime('2026-11-01T08:00:00Z'); h.events.visibilitychange();
  assert.equal(h.nodes.length,0); assert(!h.classes.has('halloween-night'));
});
test('quiet effects preference restores and the toggle is reversible', () => {
  const h=harness('2026-10-30T12:00:00Z', {quiet:true});
  assert(h.classes.has('halloween-quiet')); assert.equal(h.button.textContent,'Wake the shadows');
  h.button.click(); assert(!h.classes.has('halloween-quiet'));
  assert.equal(h.button.attrs['aria-pressed'],'false'); assert.equal(h.storage.get('aevum-halloween-quiet'),'false');
  h.button.click(); assert(h.classes.has('halloween-quiet')); assert.equal(h.button.attrs['aria-pressed'],'true');
});
test('blocked storage never blocks reading or toggling', () => {
  const h=harness('2026-10-30T12:00:00Z', {storageBlocked:true});
  assert.equal(h.nodes.length,2); h.button.click(); assert(h.classes.has('halloween-quiet'));
});
