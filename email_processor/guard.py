from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.output_parsers import GuardrailsOutputParser
from llama_index.llm_predictor import StructuredLLMPredictor
from llama_index.prompts import PromptTemplate
from llama_index.prompts.default_prompts import (
    DEFAULT_TEXT_QA_PROMPT_TMPL,
    DEFAULT_REFINE_PROMPT_TMPL,
)


# load documents, build index
documents = SimpleDirectoryReader("text.txt").load_data()
index = VectorStoreIndex(documents, chunk_size=512)
llm_predictor = StructuredLLMPredictor()


# specify StructuredLLMPredictor
# this is a special LLMPredictor that allows for structured outputs

# define query / output spec
rail_spec = """
<rail version="0.1">

<output>
    <list name="points" description="Bullet points regarding events in the author's life.">
        <object>
            <string name="explanation" format="one-line" on-fail-one-line="noop" />
            <string name="explanation2" format="one-line" on-fail-one-line="noop" />
            <string name="explanation3" format="one-line" on-fail-one-line="noop" />
        </object>
    </list>
</output>

<prompt>

Query string here.

@xml_prefix_prompt

{output_schema}

@json_suffix_prompt_v2_wo_none
</prompt>
</rail>
"""

# define output parser
output_parser = GuardrailsOutputParser.from_rail_string(
    rail_spec, llm=llm_predictor.llm
)

# format each prompt with output parser instructions
fmt_qa_tmpl = output_parser.format(DEFAULT_TEXT_QA_PROMPT_TMPL)
fmt_refine_tmpl = output_parser.format(DEFAULT_REFINE_PROMPT_TMPL)

qa_prompt = PromptTemplate(fmt_qa_tmpl, output_parser=output_parser)
refine_prompt = PromptTemplate(fmt_refine_tmpl, output_parser=output_parser)

# obtain a structured response
query_engine = index.as_query_engine(
    service_context=ServiceContext.from_defaults(llm_predictor=llm_predictor),
    text_qa_template=qa_prompt,
    refine_template=refine_prompt,
)
response = query_engine.query(
    "What are the three items the author did growing up?",
)
print(response)