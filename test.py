from groq import Groq
client = Groq(api_key="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")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Say hello"}]
)

print(response.choices[0].message.content)