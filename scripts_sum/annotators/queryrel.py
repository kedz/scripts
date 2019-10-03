from queryrel.client import QueryRelClient


class QueryRel:

    def __init__(self, port, embeddings=None):
        self.queryrel_client = QueryRelClient(port)

    def __call__(self, query, doc):

        query_content = query.content.text
        texts = [utt["source"].text.strip() for utt in doc.utterances]
        query_content_inputs = [
            {"src": text, "query": query_content}
            for text in texts
        ]
        
        query_content_scores = self.queryrel_client.get_relevance(
            query_content_inputs)
        query_content_scores = [
            x if x == x else 0.0
            for x in query_content_scores
        ]
        
        if query.semantic_constraint is not None:

            sc = query.semantic_constraint.text
            sc_inputs = [
                {"src": text, "query": sc}
                for text in texts
            ]
            sc_scores = self.queryrel_client.get_relevance(
                sc_inputs)

            sc_scores = [
                x if x == x else 0.0
                for x in sc_scores
            ]
 
        else:
            sc_scores = [None] * len(texts)

        annotations = [
            {"query_content": s1, "semantic_constraint": s2}
            for s1, s2 in zip(query_content_scores, sc_scores)
        ]

        meta = {
            "query": query.string,
            "type": "QueryRel", 
        }

        return {"annotation": annotations, "meta": meta}