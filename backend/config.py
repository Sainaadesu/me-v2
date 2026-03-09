# llama3:8b-instruct-q4_K_M ai моделийн загвар
MODEL_NAME = "llama3:latest" 
# memory дахь утгуудийг тоон утга болгох загвар
EMBED_MODEL = "nomic-embed-text"
# memory дахь гаргасан тоон утгуудийг хадгалах өгөгдлийн сангийн зам
VECTOR_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "sainaa_memory"
# хэрэглэгчийн оруулсан асуулттай хамгийн ойр 5 memory-г авна default: 5
TOP_K = 5
# ai-ийн нэг удаагийн чатний хэмжээ программ ажиллах хугацаатай холбоотой default: 400
CHUNK_SIZE = 400
# хэрэглэгч болон түүний асуулттай холбоотой текс мэдээллийг авах хэмжээ default: 2048
CONTEXT_SIZE = 2048
# уг ai-ийг ажиллуулах thread-ийн тоо, хэрэв компьютерийнхээ thread-ийн тоогоор тохируулбал илүү хурдан ажиллах боломжтой
#default: 4
THREADS = 4