---
type: llm
focus: { source: file, path: drafts/example-domains.style-check/facts/ledger.json }
---

The file is a fact-check ledger for a short essay. Its draft claims that IANA reserves example.com, example.net, and example.org for documentation (true), that IANA sells these domains to companies that ask early, citing IANA's example domains page (false: the page says the domains are reserved and not available for registration or transfer), and that "Tim Berners-Leigh" proposed the World Wide Web in 1989 (the year is right; the name is Berners-Lee).

PASS if the row for the claim that IANA sells the domains has the verdict contradicted, unsupported, or link-mismatch, and no row marks that claim confirmed.
FAIL if that claim is missing from the ledger, or is marked confirmed or link-dead.
