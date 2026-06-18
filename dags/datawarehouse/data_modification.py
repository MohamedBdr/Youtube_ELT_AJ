import logging

logger = logging.getLogger(__name__)
table = "yt_api"

def insert_rows(cur, conn, schema, row):
    try:
        if schema == "staging":
            cur.execute(f'''
                INSERT INTO {schema}.{table}
                ("video_id", "video_title", "upload_date", "duration", "video_views", "likes_count", "comments_count")
                VALUES (
                    %(video_id)s,
                    %(title)s,
                    %(publishedAt)s,
                    %(duration)s,
                    %(viewCount)s,
                    %(likeCount)s,
                    %(commentCount)s
                );
            ''', row)

        else:
            cur.execute(f'''
                INSERT INTO {schema}.{table}
                ("video_id", "video_title", "upload_date", "duration", "video_type", "video_views", "likes_count", "comments_count")
                VALUES (
                    %(video_id)s,
                    %(video_title)s,
                    %(upload_date)s,
                    %(duration)s,
                    %(video_type)s,
                    %(video_views)s,
                    %(likes_count)s,
                    %(comments_count)s
                );
            ''', row)

        conn.commit()

    except Exception as e:
        logger.error(f"Insert error Video_ID={row.get('video_id')}: {e}")
        raise

def update_rows(cur, conn, schema, row):

    try:
        # staging
        if schema == "staging":
            Video_ID = 'video_id'
            Video_Title = 'title'
            Upload_Date = 'publishedAt'
            Duration = 'duration'
            Video_Views = 'viewCount'
            Likes_Count = 'likeCount'
            Comments_Count = 'commentCount'
        # Core
        else:
            Video_ID = 'video_id'
            Video_Title = 'video_title'
            Upload_Date = 'upload_date'
            Duration = 'duration'
            Video_Views = 'video_views'
            Likes_Count = 'likes_count'
            Comments_Count = 'comments_count'
        
        cur.execute(f'''
            UPDATE {schema}.{table}
            SET
                "video_title" = %({Video_Title})s,
                "video_views" = %({Video_Views})s,
                "likes_count" = %({Likes_Count})s,
                "comments_count" = %({Comments_Count})s
            WHERE
                "video_id" = %({Video_ID})s
                AND "upload_date" = %({Upload_Date})s;
            ''', row)

        conn.commit()
        logger.info(f"Update row with Video_ID: {row['video_id']}")

    except Exception as e:
        logger.error(f"Error updating row with Video_ID: {row['video_id']} - {e}")
        raise e
    
def delete_rows(cur, conn, schema, ids_to_delete):
    try:
        ids_to_delete = f"""({", ".join(f"'{id}'" for id in ids_to_delete)})"""

        cur.execute(
            f'''
            DELETE FROM {schema}.{table}
            WHERE "video_id" IN {ids_to_delete}
        '''
        )

        conn.commit()
        logger.info(f"Update row with Video_ID: {ids_to_delete}")

    except Exception as e:
        logger.error(f"Error updating row with Video_ID: {ids_to_delete} - {e}")
        raise e