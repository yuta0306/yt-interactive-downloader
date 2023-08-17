import time
from typing import Any, Final, Literal

import requests
from tqdm import tqdm


class YouTube:
    SEARCH_ENDPOINT: Final[str] = "https://www.googleapis.com/youtube/v3/search"
    PLAYLISTITEMS_ENDPOINT: Final[
        str
    ] = "https://www.googleapis.com/youtube/v3/playlistItems"

    def __init__(self, key: str) -> None:
        self.__key = key

    def search(
        self,
        *,
        part: Literal["id", "snippet"] = "snippet",
        filter: Literal[
            "forContentOwner", "forMine", "relatedToVideoId"
        ] = "forContentOwner",
        relatedToVideoId: str | None = None,
        channelId: str | None = None,
        channelType: str | None = None,
        maxResults: int = 5,
        onBehalfOfContentOwner: str | None = None,
        order: str | None = None,
        pageToken: str | None = None,
        publishedAfter: str | None = None,
        publishedBefore: str | None = None,
        q: str | None = None,
        regionCode: str | None = None,
        safeSearch: str | None = None,
        topicId: str | None = None,
        type: str | None = None,
        videoCaption: str | None = None,
        videoCategoryId: str | None = None,
        videoDefinition: str | None = None,
        videoDimension: str | None = None,
        videoDuration: str | None = None,
        videoEmbeddable: str | None = None,
        videoLicense: str | None = None,
        videoSyndicated: str | None = None,
        videoType: str | None = None,
        time_sleep: float = 0.5,
    ) -> tuple[dict[str, Any], int]:
        """
        Parameters
        ----------
        part : str
            part パラメータには、API レスポンスに含める 1 つまたは複数の search リソースのプロパティをカンマ区切りリストの形式で指定します。
            このパラメータに指定できる part 名は id と snippet です。
            このパラメータに子プロパティを持つプロパティが指定されている場合、その子プロパティもレスポンスに含まれます。
            たとえば、search の結果では、snippet プロパティには、結果のタイトルや説明などを識別する別のプロパティが含まれます。
            この場合、part=snippet と設定すると、API レスポンスには、ネストされているプロパティもすべて含まれることになります。
        channelId : str, optional
            channelId パラメータは、チャンネルによって作成されたリソースのみが API レスポンスに含まれるように指定します。
        channelType : str, optional
            channelType パラメータでは、検索対象を特定のタイプのチャンネルに制限できます。
            以下の値を指定できます。
            - any – すべてのチャンネルを返します。
            - show – 番組のみを取得します。
            - eventType	string
                eventType パラメータは、検索対象をブロードキャスト イベントに制限します。

                以下の値を指定できます。
                - completed – 完了したブロードキャストのみを含めます。
                - live – アクティブなブロードキャストのみを含めます。
                - upcoming – 今後配信予定のブロードキャストのみを含めます。
        maxResults : int, default=5
            maxResults パラメータには、結果セットとして返されるアイテムの最大数を指定します。0 以上 50 以下の値を指定できます。デフォルト値は 5 です。
        onBehalfOfContentOwner : str, optional
            このパラメータは、適切に承認されたリクエストでのみ使用できます。注: このパラメータは、YouTube コンテンツ パートナー専用です。

            onBehalfOfContentOwner パラメータは、リクエストの承認用認証情報が、パラメータ値で指定されたコンテンツ所有者の代理人である YouTube CMS ユーザーのものであることを示します。
            このパラメータは、複数の YouTube チャンネルを所有、管理している YouTube コンテンツ パートナーを対象にしています。
            このパラメータを使用すると、コンテンツ所有者は一度認証されれば、すべての動画やチャンネル データにアクセスできるようになります。
            チャンネルごとに認証情報を指定する必要はありません。ユーザー認証に使用する CMS アカウントは、指定された YouTube コンテンツ所有者にリンクされていなければなりません。
        order : str, optional
            order パラメータには、API レスポンス内のリソースの並べ替え方法を指定します。デフォルト値は SEARCH_SORT_RELEVANCE です。

            以下の値を指定できます。
            - date – リソースを作成日の新しい順に並べます。
            - rating – リソースを評価の高い順に並べます。
            - relevance – リソースを検索クエリの関連性が高い順に並べます。このパラメータのデフォルト値です。
            - title – リソースをタイトルのアルファベット順に並べます。
            - videoCount – アップロード動画の番号順（降順）にチャンネルを並べます。
            - viewCount – リソースを再生回数の多い順に並べます。
        pageToken : str, optional
            pageToken パラメータには、返される結果セットに含める特定のページを指定します。API レスポンスでは、nextPageToken と prevPageToken プロパティは取得可能な他のページを表します。
        publishedAfter : str, optional
            publishedAfter パラメータは、指定した日時より後に作成されたリソースのみが API レスポンスに含まれるように指定します。
            この値は RFC 3339 形式の date-time 値です（1970-01-01T00:00:00Z）。
        publishedBefore : str, optional
            publishedBefore パラメータは、指定した日時より前に作成されたリソースのみが API レスポンスに含まれるように指定します。
            この値は RFC 3339 形式の date-time 値です（1970-01-01T00:00:00Z）。
        q : str, optional
            q パラメータは検索クエリを指定します。
        regionCode : str, optional
            regionCode パラメータは、指定した国の検索結果を返すように API に指示します。パラメータの値は ISO 3166-1 alpha-2 の国コードです。
        safeSearch : str, optional
            safeSearch パラメータは、検索結果に標準コンテンツの他、制限コンテンツも含めるかどうかを指定します。

            以下の値を指定できます。
            - moderate – 検索結果のコンテンツに対して一定のフィルタリングを行い、少なくともアプリケーションの言語/地域で制限されているコンテンツは除外します。
            動画の内容によっては、検索結果から動画が削除されたり検索結果内での優先度が下がったりすることがあります。これはデフォルトのパラメータ値です。
            - none – YouTube は検索結果セットのフィルタリングを行いません。
            - strict – 検索結果セットから制限コンテンツをすべて除外します。動画の内容によっては、検索結果から動画が削除されたり検索結果内での優先度が下がったりすることがあります。
        topicId : str, optional
            topicId パラメータは、指定したトピックに関連するリソースのみが API レスポンスに含まれるように指定します。この値は Freebase トピック ID を識別します。
        type : str, optional
            type パラメータは、検索クエリの対象を特定のタイプのリソースのみに制限します。
            値はカンマで区切られたリソースのタイプのリストです。デフォルト値は video,channel,playlist です。

            以下の値を指定できます。
            - channel
            - playlist
            - video
        videoCaption : str, optional
            videoCaption パラメータは、字幕の有無に基づいて動画の検索結果をフィルタリングするように指定します。

            以下の値を指定できます。
            - any – 字幕の有無に基づいた結果のフィルタリングを行いません。
            - closedCaption – 字幕がある動画のみを含めます。
            - none – 字幕がない動画のみを含めます。
        videoCategoryId : str, optional
            videoCategoryId パラメータは、動画の検索結果をカテゴリに基づいてフィルタリングします。
        videoDefinition : str, optional
            videoDefinition パラメータを使用すると、検索結果を HD（高解像度）または SD（標準解像度）のみに制限できます。
            HD 動画は 720p 以上で再生できます。また 1080p など、さらに高い解像度も利用できる場合があります。

            以下の値を指定できます。
            - any – 解像度に関係なく、すべての動画を返します。
            - high – HD 動画のみを取得します。
            - standard – SD 動画のみを取得します。
        videoDimension : str, optional
            videoDimension パラメータでは、検索結果を 2D 動画または 3D 動画のみに限定できます。

            以下の値を指定できます。
            - 2d – 検索結果から 3D 動画を除外します。
            - 3d – 検索結果を 3D 動画に限定します。
            - any – 返される結果に 3D 動画と 3D 以外の動画の両方を含めます。これはデフォルトの値です。
        videoDuration : str, optional
            videoDuration パラメータは、動画の検索結果を期間に基づいてフィルタリングします。

            以下の値を指定できます。
            - any – 検索結果を期間に基づいてフィルタリングしません。これはデフォルトの値です。
            - long – 20 分を超える動画のみを含めます。
            - medium – 4 分以上 20 分以下の動画のみを含めます。
            - short – 4 分未満の動画のみを含めます。
        videoEmbeddable : str, optional
            videoEmbeddable パラメータでは、Web ページに埋め込み可能な動画のみを検索するように制限できます。

            以下の値を指定できます。
            - any – 埋め込み可能かどうかにかかわらず、すべての動画を返します。
            - true – 埋め込み動画のみを取得します。
        videoLicense : str, optional
            videoLicense パラメータは、特定のライセンスがある動画のみが検索結果に含まれるようにフィルタリングします。
            YouTube では、動画をアップロードしたユーザーが、動画ごとにクリエイティブ・コモンズ ライセンスまたは標準の YouTube ライセンスを設定できます。

            以下の値を指定できます。
            - any – ライセンスの種類にかかわらず、クエリ パラメータに一致するすべての動画を返します。
            - creativeCommon – クリエイティブ・コモンズ ライセンスを持つ動画のみを返します。このライセンスを持つ動画は、動画作成時に誰でも再利用できます。詳細
            - youtube – 標準の YouTube ライセンスを持つ動画のみを返します。
        videoSyndicated : str, optional
            videoSyndicated パラメータでは、検索対象を youtube.com 以外で再生できる動画のみに限定できます。

            以下の値を指定できます。
            - any – シンジケートされているかどうかにかかわらず、すべての動画を返します。
            - true – シンジケートされている動画のみを取得します。
        videoType : str, optional
            videoType パラメータでは、検索対象を特定のタイプの動画に制限できます。

            以下の値を指定できます。
            - any – すべての動画を返します。
            - episode – 番組のエピソードのみを取得します。
            - movie – 動画のみを取得します。
        """
        max_iter = 1
        if maxResults <= 0:
            max_iter = 10000
            maxResults = 50
        if maxResults > 50:
            max_iter = maxResults // 50
            maxResults = 50

        totalResults = None
        items = []
        for _ in tqdm(range(max_iter)):
            params = {
                "key": self.__key,
                "part": part,
                "filter": filter,
                "relatedToVideoId": relatedToVideoId,
                "channelId": channelId,
                "channelType": channelType,
                "maxResults": maxResults,
                "onBehalfOfContentOwner": onBehalfOfContentOwner,
                "order": order,
                "pageToken": pageToken,
                "publishedAfter": publishedAfter,
                "publishedBefore": publishedBefore,
                "q": q,
                "regionCode": regionCode,
                "safeSearch": safeSearch,
                "topicId": topicId,
                "type": type,
                "videoCaption": videoCaption,
                "videoCategoryId": videoCategoryId,
                "videoDefinition": videoDefinition,
                "videoDimension": videoDimension,
                "videoDuration": videoDuration,
                "videoEmbeddable": videoEmbeddable,
                "videoLicense": videoLicense,
                "videoSyndicated": videoSyndicated,
                "videoType": videoType,
            }
            res = requests.get(self.SEARCH_ENDPOINT, params=params)
            res_dict = res.json()
            items.extend(res_dict["items"])
            if totalResults is None:
                totalResults = int(res_dict["pageInfo"]["totalResults"])
                print("TotalResults:", totalResults)
            pageToken = res_dict.get("nextPageToken")
            if pageToken is None:
                break
            time.sleep(time_sleep)
        res_dict["items"] = items
        print("Fetched Results:", len(items))
        return res_dict, res.status_code

    def fetch_playlist_items(
        self,
        *,
        part: Literal["id", "snippet", "contentDetails", "status"] = "snippet",
        id: str | None = None,
        playlistId: str | None = None,
        maxResults: int = -1,
        pageToken: str | None = None,
        videoId: str | None = None,
        time_sleep: float = 0.5,
    ) -> tuple[dict[str, Any], int]:
        """
        Parameters
        ----------
        part : str
            part パラメータには、API レスポンスに含める 1 つまたは複数の playlistItem リソース プロパティをカンマ区切りリストの形式で指定します。
            このパラメータ値に指定できる part 名は id、snippet、contentDetails、status などです。

            このパラメータに子プロパティを持つプロパティが指定されている場合、その子プロパティもレスポンスに含まれます。
            たとえば playlistItem リソースの snippet プロパティは、title、description、position、resourceId プロパティなどの複数のフィールドを持ちます。
            この場合、part=snippet と設定すると、API レスポンスにはこれらのプロパティすべてが含まれることになります。
        id : str, optional
            id パラメータには、1 つまたは複数の一意の再生リスト アイテム ID をカンマ区切りリストの形式で指定します。
        playlistId : str, optional
            playlistId パラメータには、再生リスト アイテムを取得する再生リストの一意の ID を指定します。
            このパラメータは省略可能ですが、再生リスト アイテムを取得するためのすべてのリクエストには id パラメータまたは playlistId パラメータのいずれかの値を指定する必要があることに注意してください。
        maxResults : int, default=-1
            playlistId パラメータには、再生リスト アイテムを取得する再生リストの一意の ID を指定します。
            このパラメータは省略可能ですが、再生リスト アイテムを取得するためのすべてのリクエストには id パラメータまたは playlistId パラメータのいずれかの値を指定する必要があることに注意してください。
        pageToken : str, optional
            pageToken パラメータには、返される結果セットに含める特定のページを指定します。API レスポンスでは、nextPageToken と prevPageToken プロパティは取得可能な他のページを表します。
        videoId : str, optional
            videoId パラメータでは、指定した動画を含む再生リスト アイテムだけをリクエストによって返すことを指定します。
        """
        if (id is None and playlistId is None) or (
            id is not None and playlistId is not None
        ):
            raise ValueError
        max_iter = 1
        if maxResults <= 0:
            max_iter = 10000
            maxResults = 50
        if maxResults > 50:
            max_iter = maxResults // 50
            maxResults = 50

        totalResults = None
        items = []
        for _ in tqdm(range(max_iter)):
            params = {
                "key": self.__key,
                "part": part,
                "id": id,
                "playlistId": playlistId,
                "maxResults": maxResults,
                "pageToken": pageToken,
                "videoId": videoId,
            }
            res = requests.get(self.PLAYLISTITEMS_ENDPOINT, params=params)
            res_dict = res.json()
            items.extend(res_dict["items"])
            if totalResults is None:
                totalResults = int(res_dict["pageInfo"]["totalResults"])
                print("TotalResults:", totalResults)
            pageToken = res_dict.get("nextPageToken")
            if pageToken is None:
                break
            time.sleep(time_sleep)
        res_dict["items"] = items
        print("Fetched Results:", len(items))
        return res_dict, res.status_code
