// utils/llm.js
// Wrapper around the Anthropic Messages API

const LLMClient = {
  API_URL: 'https://api.anthropic.com/v1/messages',
  MODEL:   'claude-sonnet-4-20250514',

  /**
   * Send a request to the Anthropic API and return the parsed JSON result.
   * @param {string} errorText - The raw Python error/traceback from the user.
   * @returns {Promise<{ meaning: string, causes: string[], fix: string, example: string }>}
   */
  async getResponse(errorText) {
    const response = await fetch(this.API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
        // Note: API key is injected by the Anthropic proxy — do not add it here.
      },
      body: JSON.stringify({
        model:      this.MODEL,
        max_tokens: 1000,
        system:     SYSTEM_PROMPT,
        messages: [
          { role: 'user', content: buildPrompt(errorText) }
        ]
      })
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err?.error?.message || `HTTP ${response.status}`);
    }

    const data = await response.json();

    // Concatenate all text blocks (defensive — usually just one)
    const raw = (data.content || [])
      .map(block => block.text || '')
      .join('');

    // Strip any accidental markdown code fences
    const clean = raw.replace(/```json|```/gi, '').trim();

    return JSON.parse(clean);
  }
};
