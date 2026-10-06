# Public status page

We need a public status page. One self-contained HTML file we can drop on any static host, generated from the services JSON that `app.status.load` already reads.

Build `app/page.py` with `render(services: list[dict], generated_at: str) -> str`, which returns the whole HTML document. `python -m app.page services.json` should print the page to stdout, using the current UTC time in ISO format as `generated_at`.

A service has `name` and `state` (`operational`, `degraded`, `outage` or `maintenance`) and may have `note`, `url` and `uptime`. Any other state is a bug in the data: raise `ValueError("unknown state: <state>")`.

## Document

Start with `<!doctype html>`, then `<html lang="en">`. The head has `<meta charset="utf-8">`, the viewport meta (`width=device-width, initial-scale=1`) and the title, which reads `Status · 3 of 4 operational` with the real counts. All CSS lives in a single `<style>` element. No external stylesheets and no scripts: the page has to work from a file.

Everything that comes from the data must be HTML-escaped.

## Header and banner

A `<header>` with an `<h1>` that says `System status`.

Under it, a banner: an element with class `banner` and `role="status"`. It says `All systems operational` when nothing is degraded or down. Otherwise it counts the services that are degraded or in outage: `2 of 4 services need attention`, or `1 of 4 services needs attention` when it is exactly one. Maintenance does not count as needing attention, but when any service is under maintenance the banner adds ` · 1 under maintenance` at the end, with the number.

The banner also carries one modifier class: `banner--down` if any service is in outage, otherwise `banner--warn` if any is degraded, otherwise `banner--ok`.

## Services

Inside `<main>`, a `<ul class="services">` with one `<li class="service">` per service. Order them by severity: outages first, then degraded, then maintenance, then operational; services in the same state go alphabetically by name, ignoring case.

Each item has:

- a `data-state` attribute with the state;
- a decorative dot, `<span class="dot" aria-hidden="true"></span>`;
- the name in an `<h2>`. If the service has a `url` the name is a link to it, and links to another site (`http://` or `https://`) get `rel="noopener"`; relative links do not;
- the state in words in a `<span class="state">`: `Operational`, `Degraded performance`, `Major outage` or `Under maintenance`;
- the note in a `<p class="note">`, only when there is one;
- the uptime as `<span class="uptime">99.98% uptime</span>`, always two decimals, only when the service has an uptime.

It would be nice if each item also had an `id` like `service-payments-api` (the name in lowercase, anything that is not a letter or digit turned into a single hyphen, no hyphen at the ends), so support can link to one service.

With no services at all there is no banner and no list: show `<p class="empty">No services configured.</p>` and make the title `Status · no services`.

## Footer

A `<footer>` with `<time datetime="...">Updated ...</time>`, where both the attribute and the text after `Updated ` are `generated_at` as given.

## Look

- Colors are custom properties on `:root`: `--bg`, `--text`, `--ok`, `--warn`, `--down` and `--maint`. Dark mode is a `@media (prefers-color-scheme: dark)` block that redefines at least `--bg` and `--text`.
- The dot takes its color from the state, with one rule per state like `[data-state="outage"] .dot`.
- The outage dot pulses: a `@keyframes pulse` animation applied to the outage dot and to no other dot. People who ask for less motion must not get it: a `@media (prefers-reduced-motion: reduce)` block sets `animation: none`.
- The list is a centered column, `max-width: 640px`.
- On phones, `@media (max-width: 480px)`, each service stacks vertically (`flex-direction: column`).
- Links show a visible outline on keyboard focus with an `a:focus-visible` rule.
- Body text uses the system font: `font-family: system-ui, sans-serif`.
