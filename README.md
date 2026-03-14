# Georgian STT Autocorrect Agent (Local-first)

ეს პროექტი ქმნის AI აგენტს, რომელიც **speech-to-text** ტექსტს ქართულად კონტექსტურად ასწორებს:
- ორთოგრაფიას
- გრამატიკას
- სიტყვათა შეთანხმებას
- მთლიანი წინადადების გამართულობას

მთავარი მოთხოვნა დაკმაყოფილებულია: გამოიყენება **open-source მოდელი**, რომელიც **უფასოდ და ლოკალურად** ჰოსტდება.

## როგორ მუშაობს

1. STT სისტემა აბრუნებს ნედლ ქართულ ტექსტს (შეცდომებით).
2. ეს აგენტი აგზავნის ტექსტს ლოკალურ LLM-ში (Ollama API-ის გავლით).
3. მოდელი აბრუნებს მხოლოდ გამართულ ქართულ ტექსტს.

## ტექნოლოგიები

- Python
- FastAPI
- Ollama (local model server)
- Open-source LLM (ნაგულისხმევი: `qwen2.5:3b-instruct`)

## მოთხოვნები

- Python 3.10+
- Ollama

### Ollama ინსტალაცია და მოდელი

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull qwen2.5:3b-instruct
```

## გაშვება

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn stt_agent.api:app --host 0.0.0.0 --port 8000
```

გაშვების შემდეგ შეგიძლიათ პირდაპირ გახსნათ:

- `http://localhost:8000/` (აბრუნებს სწრაფ ბმულებს)
- `http://localhost:8000/docs` (ინტერაქტიული Swagger UI)
- `http://localhost:8000/health` (health check)

## API გამოყენება

```bash
curl -X POST http://localhost:8000/correct \
  -H 'Content-Type: application/json' \
  -d '{"text":"დღეს მე წავედი სკოლში და მერე მოვიდა ჩვენ სახლშ"}'
```

მაგალითი პასუხი:

```json
{
  "corrected_text": "დღეს მე წავედი სკოლაში და მერე მოვიდა ჩვენს სახლში.",
  "model": "qwen2.5:3b-instruct"
}
```

## CLI გამოყენება

```bash
python -m stt_agent.cli "დღეს მე წავედი სკოლში და მერე მოვიდა ჩვენ სახლშ"
```

## შენიშვნები ხარისხზე

- უკეთესი შედეგისთვის გამოიყენეთ უფრო ძლიერი local მოდელი, მაგალითად:
  - `qwen2.5:7b-instruct`
  - `llama3.1:8b-instruct`
- დომენზე მორგებისთვის შეგიძლიათ შექმნათ დამატებითი fine-tuning/LoRA მონაცემები Georgian STT შეცდომებზე.

## ლოკალური ჰოსტინგის შესაბამისობა

ეს არქიტექტურა სრულად მუშაობს ლოკალურად:
- API სერვერი ლოკალურ მანქანაზე
- LLM inference ლოკალურ Ollama სერვერზე
- არ არის სავალდებულო paid cloud
