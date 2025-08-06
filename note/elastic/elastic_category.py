from note.documents import CategoryNotesDocument,NotesDocument
from note.serializers import CategorySearchViewSerializer, NoteSearchViewSerializer


def elastic_search_category(request):
    user_id = str(request.user.id)
    query = request.query_params.get("q", "")
    page = int(request.query_params.get("page", 1))
    page_size = int(request.query_params.get("page_size", 5))
    start = (page - 1) * page_size
    results = CategoryNotesDocument.search().query(
        "bool",
        must=[
            {
                "match_phrase_prefix": {
                    "title": {
                        "query": query,
                    }
                }
            }
        ],
        filter=[
            {
                "term": {
                    "user": user_id
                }
            }
        ]
    ).extra(from_=start, size=page_size)
    total_page = results.count()
    results = [{"id": result.meta.id,"title": result.title} for result in results]
    serializer = CategorySearchViewSerializer(results, many=True)
    return total_page, page, page_size, serializer



def elastic_search_note(request):
    user_id = str(request.user.id)
    query = request.query_params.get("q", "")
    page = int(request.query_params.get("page", 1))
    page_size = int(request.query_params.get("page_size", 5))
    start = (page - 1) * page_size
    results = NotesDocument.search().query(
        "bool",
        must=[
            {
                "match_phrase_prefix": {
                    "title": {
                        "query": query,
                    }
                }
            }
        ],
        filter=[
            {
                "term": {
                    "user": user_id
                }
            }
        ]
    ).extra(from_=start, size=page_size)
    total_page = results.count()
    results = [{"id": result.meta.id,"title": result.title} for result in results]
    serializer = NoteSearchViewSerializer(results, many=True)
    return total_page, page, page_size, serializer