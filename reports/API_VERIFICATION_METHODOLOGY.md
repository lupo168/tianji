# API Availability Verification Methodology

> Systematic process for checking if a platform offers a public API.

## URL Patterns to Check

```
developer.{platform}.{tld}/
dev.{platform}.{tld}/
developers.{platform}.{tld}/
{platform}.{tld}/api/
{platform}.{tld}/developer
```

## Government Open Data URLs

| Language | Pattern |
|----------|---------|
| Swedish | /oppna-data/ /oppnadata/ |
| Norwegian | /apne-data/ |
| English | /open-data/ /opendata/ |
| Korean | data.go.kr (unified portal) |

## Result Categories

| Mark | Meaning |
|------|---------|
| ✅ Yes | Public API with documentation |
| ⚠️ Maybe | Exists but needs further verification |
| ❌ No | No public API |
| 📡 RSS | RSS feed available |
