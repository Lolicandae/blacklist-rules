const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

function load(filename) {
  const file = path.join(__dirname, "../client_conf/mihomo_override", filename);
  return vm.runInNewContext(`${fs.readFileSync(file, "utf8")}\nmain;`, {}, { filename });
}

const original = load("mihomo_override.js");
const noDns = load("mihomo_override_no_dns.js");
const cases = [
  { proxies: [{ name: "example", type: "direct" }], dns: { enable: true, nameserver: ["192.0.2.53"], "enhanced-mode": "redir-host" }, tun: { enable: false } },
  { proxies: [{ name: "example", type: "direct" }] },
  { "proxy-providers": { example: { type: "file", path: "./example.yaml" } }, dns: null },
  { proxies: [{ name: "example", type: "direct" }], dns: { enable: false } },
];

for (const fixture of cases) {
  const input = JSON.parse(JSON.stringify(fixture));
  const dns = input.dns;
  const dnsContents = JSON.stringify(dns);
  const hasDns = Object.hasOwn(input, "dns");
  const result = noDns(input);
  assert.equal(result, input);
  assert.equal(Object.hasOwn(result, "dns"), hasDns);
  assert.equal(result.dns, dns);
  assert.equal(JSON.stringify(result.dns), dnsContents);

  const expected = original(JSON.parse(JSON.stringify(fixture)));
  delete expected.dns;
  const actual = { ...result };
  delete actual.dns;
  assert.equal(JSON.stringify(actual), JSON.stringify(expected));
}

for (const main of [original, noDns]) {
  assert.throws(() => main({}), /Cannot Find any proxy providers/);
}
console.log("No-DNS override preserves DNS and otherwise matches the original.");
