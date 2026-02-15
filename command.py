python -m pip install --upgrade --force-reinstall \
"pydantic>=2.11,<3" \
"pydantic-core==2.33.2" \
"python-multipart>=0.0.9" \
"uvicorn>=0.31.1" \
"langchain-core>=0.3.36" \
"langchain-mcp-adapters>=0.1.9" \
"langgraph>=0.6.7,<0.7" \
"langgraph-prebuilt>=0.6,<0.7" \
"opentelemetry-sdk==1.39.1" \
"opentelemetry-semantic-conventions>=0.60b1"



python - <<'EOF'
import pydantic, pydantic_core, langgraph, langgraph_prebuilt, uvicorn
import sys
print("python:", sys.executable)
print("pydantic:", pydantic.__version__, pydantic.__file__)
print("pydantic-core:", pydantic_core.__version__, pydantic_core.__file__)
print("langgraph:", langgraph.__version__, langgraph.__file__)
print("langgraph-prebuilt:", langgraph_prebuilt.__version__, langgraph_prebuilt.__file__)
print("uvicorn:", uvicorn.__version__, uvicorn.__file__)
EOF


python -m pip install --upgrade --force-reinstall "huggingface-hub>=0.20" transformers "numpy<2"
