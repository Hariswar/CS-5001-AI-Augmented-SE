# Classroom CLI Agent (cca) - Ollama-only

Default model: devstral-small-2:24b-cloud
Override:
- --model <name>
- OLLAMA_MODEL environment variable

## Install
pip install -e .

## Start Ollama and pull model
ollama serve
ollama pull devstral-small-2:24b-cloud

## Example repo (make sure it is a git repo)
cd demo_repo
git init
git add -A
git commit -m "init demo repo"
cd ..

## Create a program
cca  --repo demo_repo create   --desc "A calculator with add, subtract, multiply, divide functions"   --module src/calculator.py

## Generate tests and iterate until target coverage (natural language)
cca --repo output/demo_repo test --desc "A calculator with add, subtract, multiply, divide functions"   --module src/calculator.py   --tests tests/test_calculator.py   --coverage "90 percent"

## Commit and push
cca --repo output/demo_repo commit --message "Agent: add program + tests" --push

## End-to-end
cca --repo output/demo_repo full --desc "A calculator with add, subtract, multiply, divide functions" --module src/calculator.py --tests tests/test_calculator.py --coverage "at least ninety five percent" --message "Agent: add program + tests" --push
