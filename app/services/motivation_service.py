from app.extensions import SessionLocal
from app.models.motivation import Motivation
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response

def create_fashion_advice(skin_tone: str, total: int):
    session = SessionLocal()

    try:
        prompt = f"""
        Anda adalah pakar fashion stylist. Dalam format JSON, buat {total} saran perpaduan warna pakaian yang sangat cocok untuk seseorang dengan warna kulit "{skin_tone}".
        Setiap saran harus mencakup atribut berikut:
        - Baju
        - Celana
        - Dalaman (Kaos dalam)
        - Kaos kaki
        - Sepatu
        - Jaket atau Jas

        Format JSON harus seperti ini:
        {{
            "motivations": [
                {{
                    "text": "Baju: [warna], Celana: [warna], Dalaman: [warna], Kaos kaki: [warna], Sepatu: [warna], Jaket/Jas: [warna]"
                }}
            ]
        }}
        PENTING: Hanya berikan JSON, jangan ada teks penjelasan lain. Gunakan bahasa Indonesia.
        """

        result = generate_from_llm(prompt)
        recommendations = parse_llm_response(result)

        # save request log (menggunakan field theme untuk menyimpan skin_tone)
        req_log = RequestLog(theme=skin_tone)
        session.add(req_log)
        session.commit()

        saved = []

        for item in recommendations:
            text = item.get("text")

            m = Motivation(
                text=text,
                request_id=req_log.id
            )
            session.add(m)
            saved.append(text)

        session.commit()

        return saved

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def get_all_fashion_advice(page: int = 1, per_page: int = 100):
    session = SessionLocal()

    try:
        query = session.query(Motivation)

        total = query.count()

        data = (
            query
            .order_by(Motivation.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        result = [
            {
                "id": m.id,
                "text": m.text,
                "created_at": m.created_at.isoformat()
            }
            for m in data
        ]

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "data": result
        }

    finally:
        session.close()
