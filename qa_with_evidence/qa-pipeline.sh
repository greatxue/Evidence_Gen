# Activate environment and change directory
conda init
conda activate llm_uncer

# Common Variables
BASE_DIR="/home/wenhao/Project/greatxue/llm_uncer"
EVIDENCE_DIR="${BASE_DIR}/evidence"
OUTPUT_JSON_DIR="${BASE_DIR}/output/json"
OUTPUT_MERGED_DIR="${BASE_DIR}/output/merged_json"
EVIDENCE_FILE="${EVIDENCE_DIR}/1031-evi-bookqa-qwen.txt"
TIMESTAMP="11030128"
DATASET_NAME="openbookqa"
MODEL_NAME="qwen1.5-7b-chat"

cd "${BASE_DIR}/qa_with_evidence"

# Step 1: Generate the model evidence (Update your TODO script path as needed)
# python3 1-qa-evidencer.py --dataset_name "$DATASET_NAME" \
#     --model "$MODEL_NAME" \
#     --output_path "${EVIDENCE_FILE}"

# Step 2: Query the model for the output JSON
for PROMPT_TYPE in "direct" "CoT" "evidenceCoT" "evidence"
do
    OUTPUT_FILE="${OUTPUT_JSON_DIR}/${TIMESTAMP}-${DATASET_NAME}-${MODEL_NAME}-${PROMPT_TYPE}.json"
    python3 2-qa-ans.py --dataset_name "$DATASET_NAME" \
        --model "$MODEL_NAME" \
        --evidence_path "$EVIDENCE_FILE" \
        --prompt_type "$PROMPT_TYPE" \
        --output_path "$OUTPUT_FILE"
done

# Step 3: Combine the JSON results and retrieve the choices
python3 3-qa-merge.py --input_path "${OUTPUT_JSON_DIR}/${TIMESTAMP}-${DATASET_NAME}-${MODEL_NAME}-direct.json" \
    "${OUTPUT_JSON_DIR}/${TIMESTAMP}-${DATASET_NAME}-${MODEL_NAME}-CoT.json" \
    "${OUTPUT_JSON_DIR}/${TIMESTAMP}-${DATASET_NAME}-${MODEL_NAME}-evidence.json" \
    "${OUTPUT_JSON_DIR}/${TIMESTAMP}-${DATASET_NAME}-${MODEL_NAME}-evidenceCoT.json" \
    --output_path "${OUTPUT_MERGED_DIR}/${TIMESTAMP}-${DATASET_NAME}-merged.json" \
    --marked_path "${OUTPUT_MERGED_DIR}/${TIMESTAMP}-${DATASET_NAME}-marked.json"

# Step 4: Evaluate the final effects
python3 4-qa-eval.py \
    --input_path "${OUTPUT_MERGED_DIR}/${TIMESTAMP}-${DATASET_NAME}-marked.json" \
    --output_path "${OUTPUT_MERGED_DIR}/${TIMESTAMP}-${DATASET_NAME}.txt"





