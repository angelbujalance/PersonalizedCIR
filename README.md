# PersonalizedCIR
A code base for personalized conversational query reformulation.

# Environment Dependency

Main packages:
- python 3.8
- torch 1.8.1
- transformer 4.2.0
- numpy 1.22
- faiss-gpu 1.7.2
- pyserini 0.16
- openai

# Runing Steps

## 1. Download data and Preprocessing

Four public datasets can be downloaded from TREC Interactive Knowledge Assistance Track (iKAT)(https://www.trecikat.com/).

## 2. Generate reformulation
There are two approaches: one involves the selection of ptkb followed by the generation of a reformulation using the chosen ptkb, while the other entails the concurrent output of both the selected ptkb and the reformulation by the LLM.

### 2.1 Select ptkb
Using LLM to select or machine choose(Add a ptkb in sequence and select the ptkb with improved scores compared to not adding it.)

    python generate_session_data_dial-level.py
    python generate_augmented_query.py

### 2.2 Generate reformulation using the selected ptkb
Generate a reformulation using the selected ptkb.(Two types of prompt)

    python generate_session_data_dial-level.py
    python generate_augmented_query.py

### 2.3 Selecte and reformulate
Simultaneously output selected ptkb and reformulation.

    python generate_session_data_dial-level.py
    python generate_augmented_query.py
    
## 3. Retrieval Indexing (Dense and Sparse)

To evaluate the trained model by ConvSDG, we should first establish index for both dense and sparse retrievers.

### 3.1 Dense
For dense retrieval, we use the pre-trained ad-hoc search model ANCE to generate passage embeedings. Two scripts for each dataset are provided by running:

    python dense_index.py

### 3.2 Sparse

For sparse retrieval, we first run the format conversion script as:

    python convert_to_pyserini_format.py
    
Then create the index for the collection by running

    bash create_index.sh

## 4. Generate Supervision Signals
The supervision signals assigned for dialogue-level generated data (for unsupervised w/o relevance judgment) are run by the following commands based on both sparse and dense retrieval.

    python search_relevant_p_sparse.py
    python search_relevant_p_dense.py

For the query-level generated data (for semi-supervised w/. relevance judgment), we directly use the original annotations as supervision signals. Thus, after generating the augmented query data, run the following command for combination:

    python preprocess_cast_augmented.py

## 5. Conversational Dense Retrieval Fine-tuning
To conduct conversational dense retrieval fine-tuning, please run the following commands. The pre-trained language model we use for dense retrieval is [ANCE](https://github.com/microsoft/ANCE).

    python train_conretriever(_augment).py --pretrained_encoder_path="checkpoints/ad-hoc-ance-msmarco" \ 
      --train_file_path=$train_file_path \ 
      --log_dir_path=$log_dir_path \
      --model_output_path=$model_output_path \ 
      --per_gpu_train_batch_size=16 \ 
      --num_train_epochs=5 \
      --max_query_length=64 \
      --max_doc_length=384 \ 
      --max_concat_length=512 \
      --is_train=True \

## 6. Retrieval evaluation

Now, we can perform retrieval to evaluate the ConvHACL-trained dense retriever by running:

    python test_retrieval_cast.py --pretrained_encoder_path=$trained_model_path \ 
      --passage_embeddings_dir_path=$passage_embeddings_dir_path \ 
      --passage_offset2pid_path=$passage_offset2pid_path \
      --qrel_output_path=$qrel_output_path \ % output dir
      --output_trec_file=$output_trec_file \
      --trec_gold_qrel_file_path=$trec_gold_qrel_file_path \ % gold qrel file
      --per_gpu_train_batch_size=4 \ 
      --test_type=convq \ 
      --max_query_length=64 \
      --max_doc_length=384 \ 
      --max_concat_length=512 \ 
      --is_train=False \
      --top_k=100 \
      --rel_threshold=1 \ # 2 for CAsT-20 and CAsT-21
      --passage_block_num=$passage_block_num \
      --use_gpu=True
