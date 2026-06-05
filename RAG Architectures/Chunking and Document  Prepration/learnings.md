# eRAG: Chunking & Document Preparation (Short Notes)

## RAG Prepare Pipeline

```text
Load → Chunk → Attach Metadata → Embed → Store (Chroma) → Retrieve
```

Purpose: Convert large documents into searchable chunks before retrieval.

---

# Why Chunking Matters

### Problem with Whole Document Embedding

- One PDF = One Vector ❌
- Multiple topics get mixed together.
- Search becomes vague and inaccurate.

### Goal

Each chunk should contain roughly **one idea/topic**.

Example:

- Return Policy → one chunk
- Shipping Policy → another chunk
- Warranty Policy → another chunk

---

# Chunking Strategies

## 1. Fixed Size + Overlap (Main Lab)

Most common beginner approach.

```python
chunk_size = 500
overlap = 75
```

Process:

```text
Chunk 1: 0–500
Chunk 2: 425–925
Chunk 3: 850–1350
```

Step size:

```python
step = chunk_size - overlap
```

### Advantages

- Easy to implement
- Easy to debug
- Works well for policies and FAQs

---

## 2. Sentence-Aware Chunking

- Split into sentences first.
- Combine sentences until size limit reached.

### Advantage

Doesn't cut in the middle of a sentence.

### Drawback

More complex.

---

## 3. Page-Based Chunking

```text
1 PDF page = 1 chunk
```

Good for short pages.

Not ideal for long pages.

---

# Chunk Size

## Definition

Maximum length of a chunk before creating the next chunk.

### Recommended

```python
chunk_size = 500
```

### Too Small (~80 chars)

❌ Loses context

Example:

```text
"within 30 days"
```

No idea what it refers to.

### Too Large (~4000 chars)

❌ Multiple topics merged

❌ Poor retrieval

---

# Chunk Overlap

## Definition

Repeated text shared between neighboring chunks.

### Recommended

```python
chunk_overlap = 75
```

Approximately:

```text
10% – 20% of chunk size
```

### Why?

Prevents information loss at chunk boundaries.

Example:

```text
Chunk 1 ends:
"...return products within"

Chunk 2 starts:
"within 30 days..."
```

Without overlap, important context may disappear.

### Rule

```python
overlap < chunk_size
```

Otherwise splitter never advances.

---

# Metadata

## Purpose

Tracks where a chunk came from.

Metadata is NOT embedded.

Metadata is stored alongside vectors.

### Required Fields

```python
{
  "source_id": "returns_policy.txt",
  "page": 0,
  "chunk_index": 1
}
```

### Benefits

- Citations
- Debugging
- Filtering
- Traceability

Example answer:

```text
Source: returns_policy.txt
Page: 0
```

instead of

```text
"Some document says..."
```

---

# Chunk IDs

Stable unique identifier:

```python
{source_id}__p{page}__c{chunk_index}
```

Example:

```text
returns_policy.txt__p0__c0
```

---

# Chunking Function

```python
def chunk_text(text, chunk_size=500, overlap=75):
    if chunk_size <= overlap:
        raise ValueError()

    chunks = []
    start = 0

    while start < len(text):
        chunks.append(
            text[start:start+chunk_size]
        )
        start += chunk_size - overlap

    return chunks
```

---

# Creating Searchable Chunks

Each chunk stores:

```python
{
  "id": "...",
  "text": "...",
  "metadata": {
      "source_id": "...",
      "page": 0,
      "chunk_index": 0
  }
}
```

---

# Chroma Storage Pipeline

## 1. Create Collection

```python
collection = client.get_or_create_collection(
    name="policy_chunks",
    embedding_function=None
)
```

---

## 2. Generate Embeddings

Model:

```python
all-MiniLM-L6-v2
```

```python
model.encode(documents)
```

---

## 3. Upsert

```python
collection.upsert(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings
)
```

---

# Retrieval

User query:

```text
How many days do I have to return a product?
```

### Steps

```text
Query
 ↓
Embed Query
 ↓
Vector Search
 ↓
Top-k Chunks Returned
```

Example:

```python
results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)
```

---

# Always Check Metadata

After retrieval:

```python
results["metadatas"]
```

Look for:

```python
source_id
page
chunk_index
```

before trusting the answer.

---

# Troubleshooting Retrieval

| Problem | Cause | Fix |
|----------|--------|------|
| Vague results | Chunk too large | Reduce chunk_size |
| Missing context | Overlap too small | Increase overlap |
| Duplicate chunks | Overlap too high | Reduce overlap |

---

# LangChain PDF Pipeline

Load all PDFs:

```python
PyPDFDirectoryLoader()
```

Split:

```python
RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=16
)
```

Store:

```python
Chroma.from_documents()
```

Pipeline:

```text
PDF Folder
    ↓
Load
    ↓
Chunk
    ↓
Embed
    ↓
Chroma
```

---

# Semantic Chunking (Advanced)

Instead of fixed-size chunks:

1. Split into sentences
2. Embed each sentence
3. Group similar sentences together

### Advantages

- Better topic boundaries
- More meaningful chunks

### Disadvantages

- More computation
- More complexity

For this module:

✅ Use Fixed Size + Overlap

---

# Vector Databases

Purpose:

Fast similarity search over embeddings.

Examples:

- Chroma
- Pinecone
- Weaviate
- FAISS

### Analogy

Like a database index:

```text
SQL → B-Tree Index
RAG → Vector Index
```

Without indexing:

```text
Query must compare against every vector.
```

With indexing:

```text
Nearest vectors found quickly.
```

---

# Exam / Interview Revision

### Core RAG Prepare Pipeline

```text
Load
↓
Chunk
↓
Metadata
↓
Embed
↓
Store
↓
Retrieve
```

### Recommended Values

```python
chunk_size = 500
chunk_overlap = 75
model = "all-MiniLM-L6-v2"
```

### Metadata Fields

```python
source_id
page
chunk_index
```

### Most Important Rule

```text
One chunk ≈ One idea
```

### Golden Formula

```python
step = chunk_size - overlap
```