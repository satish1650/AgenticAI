from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent

GEMINI = 'gemini-2.0-flash'

def make_translator_agent(lang_code, output_key):
    return LlmAgent(
        name=f'Transalor_Agent_{lang_code}',
        model=GEMINI,
        instruction=f'Create a localized marketing tagline in {lang_code} for the user’s product/idea. Return only the tagline text.',
        output_key=output_key,
    )

# Market-focused (not translation): generate localized taglines per audience
spanish = make_translator_agent('Spanish', 'es')
french = make_translator_agent('French', 'fr')
german = make_translator_agent('German', 'de')

parallel_translate = ParallelAgent(
    name='Parallel_Translator',
    description='Generate localized marketing taglines for Spanish, French, and German audiences.',
    sub_agents=[spanish, french, german],
)

merger_agent = LlmAgent(
    name='Merger_Agent',
    model=GEMINI,
    instruction='''Package the taglines neatly:
     **Spanish** {es}
     **French** {fr}
     **German** {de}

     Return the response in the following JSON format:
     ```
     {
       "es": "tagline_text",
       "fr": "tagline_text",
       "de": "tagline_text"
     }
     ```
    ''',
    output_key='merged_translation',
)

pipeline = SequentialAgent(
    name='Translation_Pipeline',
    sub_agents=[parallel_translate, merger_agent]
)

root_agent = pipeline
