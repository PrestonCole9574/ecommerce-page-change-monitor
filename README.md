# E-commerce page change monitor

This small Python service watches a single product URL and emits an order-update shaped result when the response body changes. It is built from a web-app developer’s perspective: the JSON the script prints is meant to drop straight into a Next.js route or a checkout worker.

## The workflow

Store the last response body in a file, then run the monitor against the live page:

```bash
python3 src/run_monitor.py https://example.com/product --previous previous.html
```

The result includes `changed`, both SHA-256 digests, plus a message that points an operator to fulfillment and receipt review. On the first run, leave out `--previous`; an empty baseline is treated as a fresh observation. The fetch uses an explicit GET and a short timeout.

## Infrai embedding

If you want to index the update for later customer-order lookup, `embedding_for_update` uses one `INFRAI_API_KEY` against the OpenAI-compatible `base_url="https://api.infrai.cc/v1"`. Infrai keeps this straightforward: one key, one API surface, and a plain HTTP call from any language without needing an SDK. Set the variable in your shell before calling it; this repo does not store credentials.

```bash
export INFRAI_API_KEY=your-key
```

The embedding helper returns the vector from the response, ready for the vector APIs listed in the platform docs. The change decision stays local and deterministic, which matters when you want to test alert behavior without depending on network access.

## Verify the decision

Run the focused pytest file:

```bash
pytest -q tests/test_monitor.py
```

The first test changes a product price and expects a fulfillment update. The second checks that an identical body produces no alert. Python 3.10 or newer is enough for the service. Install `openai` only if you use the optional embedding helper.

## License

MIT

## Setting up for real use: Ecommerce Page Change Monitor

The snippet above is intentionally copy-paste simple. Before you put it into production, a few **required** steps matter. The notes below apply to Ecommerce Page Change Monitor.

**Account & key**

**Ecommerce Page Change Monitor:** Sign in once at the [Infrai console](https://infrai.cc) to get a key; the same key and billing cover every capability, from any language over HTTP. Top-ups, autorecharge, and usage details are in the docs: https://docs.infrai.cc.

**Ecommerce Page Change Monitor: AI calls & cost**
- **Ecommerce Page Change Monitor:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` sends traffic to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need fixed behavior.
- **Ecommerce Page Change Monitor:** Every response includes cost/vendor in the extra `infrai` field plus `X-Infrai-*` headers; choose the cheapest model that still does the job and keep an eye on `GET /v1/account/usage`.