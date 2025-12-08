# wp3-hackathon

Hackathon for Work Package 3, with representatives from Västra Götalandsregionen, Region Stockholm and Region Skåne.

## Setup

### Installation

Clone repo:

```bash
git clone https://github.com/isak-b/wp3-hackathon.git
cd wp3-hackathon
```

Create Virtual Environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

### Configure the Azure OpenAI API

Export the following environment variables:

```bash
export AZURE_OPENAI_ENDPOINT="your azure openai endpoint (see notes)"
export AZURE_OPENAI_API_KEY="your azure openai api key (see notes)"
```

NOTE:

- Note that your Azure API-key and endpoint depends on what Azure subscription you use.
- Ask Isak or whoever manages your Azure subscription for a key and endpoint.

#### Recommended Azure OpenAI models

| Use case                   | Model(s)               |
| -------------------------- | ---------------------- |
| Text                       | gpt-4o, gpt-5.1        |
| Reasoning                  | o1, o1-mini, o3-mini   |
| Text-to-Image              | dall-e-3               |
| Image-to-Text              | gpt-4o, gpt-4o-mini    |
| Text-to-Speech             | tts, tts-hd            |
| Speech-to-Text             | whisper                |
| Text Embeddings/Vectorizer | text-embedding-ada-002 |

NOTE:

- Note that what models you have available depend on what Azure subscription you use.
- Ask Isak or whoever manages your Azure subscription for specific model recommendations and their names.

## Examples

See `notebooks/` for examples on how to do different things with langchain and langgraph.

Note that the examples were not created for this hackathon specifically, so they may or may not be relevant.

Also see [Isak's LLM notebooks](https://github.com/isak-b/llm-notebooks) for more examples.
