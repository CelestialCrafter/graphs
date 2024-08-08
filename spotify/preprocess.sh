if [ -z $1 ]; then
	echo "no dataset name specified"
	exit
fi

out="$1.txt"

set +f
cd data/
cat Streaming_History_Audio_*  |\
	jq -s 'flatten(1)' |\
jq -r 'map(select(.master_metadata_album_artist_name != null) | "\(.master_metadata_album_artist_name)|\(.ts | fromdate)") | .[]' |\
kakasi -H a -K a -J a > $out

