import webbrowser
import yt_dlp


def get_first_youtube_link(query):
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'force_generic_extractor': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_url = f"ytsearch1:{query}"
                info = ydl.extract_info(search_url, download=False)
                
                if 'entries' in info and len(info['entries']) > 0:
                    return info['entries'][0]['url']
                return None
    
            return get_first_youtube_link(query)