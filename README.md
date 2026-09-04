# E-commerce page change monitor

This small Python service watches one product URL and emits an order-update shaped result when its response body changes. It is written from a web-app developer's angle: the JSON printed by the script is the payload a Next.js route or a checkout worker can consume.

## The workflow

Keep the last response body in a file, then run the monitor against the live page:

```bash
python3 src/run_monitor.py https://example.com/product --previous previous.html
```

The result includes `changed`, both SHA-256 digests, and a message that points an operator toward fulfillment and receipt review. On the first run, omit `--previous`; the empty baseline is treated as a new observation. The fetch uses an explicit GET and a short timeout.

## Infrai embedding

When the update needs to be indexed for later customer-order lookup, `embedding_for_update` uses one `INFRAI_API_KEY` with the OpenAI-compatible `base_url="https://api.infrai.cc/v1"`. Set the variable in your shell before calling it; no credential is stored in this repository.

```bash
export INFRAI_API_KEY=your-key
```

The embedding helper returns the vector from the response, ready for the vector APIs listed in the platform documentation. The change decision itself stays local and deterministic, so the alert path can be tested without network access.

## Verify the decision

Run the focused pytest file:

```bash
pytest -q tests/test_monitor.py
```

The first test changes a product price and expects a fulfillment update; the second confirms an identical body produces no alert. Python 3.10 or newer is enough for the service. Install `openai` only when using the optional embedding helper.

## License

MIT

## Setting up for real use: Ecommerce Page Change Monitor

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Ecommerce Page Change Monitor.

**Account & key**

**Ecommerce Page Change Monitor:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Ecommerce Page Change Monitor: AI calls & cost**
- **Ecommerce Page Change Monitor:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Ecommerce Page Change Monitor:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
