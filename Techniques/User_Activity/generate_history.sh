#!/bin/zsh

BROWSERS=(
    "Safari"
    "Firefox"
    "Google Chrome"
    "Brave Browser"
)

URLS=(
    "https://www.youtube.com/watch?v=rpqZTgSters"  # Fred Again - Marea (We’ve Lost Dancing)
    "https://www.youtube.com/watch?v=J77YEV9JdEI"  # Fred Again - Delilah (pull me out of this)
    "https://www.youtube.com/watch?v=aVw4F-_ZiPc"  # Fred Again - Billie (Loving Arms)
    "https://www.youtube.com/watch?v=Q22MCFC0CP0"  # Fred Again - Turn On The Lights again..
    "https://www.youtube.com/watch?v=7wtfhZwyrcc"  # Imagine Dragons - Believer
    "https://www.youtube.com/watch?v=fKopy74weus"  # Imagine Dragons - Thunder
    "https://www.youtube.com/watch?v=ktvTqknDobU"  # Imagine Dragons - Radioactive
    "https://www.youtube.com/watch?v=gOsM-DYAEhY"  # Imagine Dragons - Whatever It Takes
    "https://www.youtube.com/watch?v=3EoI-6lQFIE"  # Kanye West - Stronger
    "https://www.youtube.com/watch?v=Co0tTeuUVhU"  # Kanye West - Heartless
    "https://www.youtube.com/watch?v=Bm5iA4Zupek"  # Kanye West - Runaway ft. Pusha T
    "https://www.youtube.com/watch?v=6CHs4x2uqcQ"  # Kanye West - Ultralight Beam
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rickroll

    "https://www.facebook.com/Google"    # Google Facebook page
    "https://www.facebook.com/Twitter"   # Twitter Facebook page
    "https://www.facebook.com/Instagram" # Instagram Facebook page
    "https://www.facebook.com/Spotify"   # Spotify Facebook page
    "https://www.facebook.com/Netflix"   # Netflix Facebook page

    "https://www.google.com/search?q=latest+tech+news"  # Google Search for latest tech news
    "https://www.google.com/search?q=how+to+learn+programming"  # Google Search for programming tutorial
    "https://www.google.com/search?q=best+restaurants+near+me"  # Google Search for local restaurants
    "https://www.google.com/search?q=weather+forecast"  # Google Search for weather forecast
    "https://www.google.com/search?q=how+to+make+money+online"  # Google Search for making money
    "https://www.google.com/search?q=top+movies+2024"  # Google Search for top movies
    "https://www.google.com/search?q=how+to+meditate"  # Google Search for meditation guide
    "https://www.google.com/search?q=travel+destinations"  # Google Search for travel ideas

    "https://www.amazon.com"  # Amazon homepage
    "https://www.reddit.com"  # Reddit homepage
    "https://www.wikipedia.org"  # Wikipedia homepage
    "https://www.twitter.com"  # Twitter homepage
    "https://www.instagram.com"  # Instagram homepage
    "https://www.linkedin.com"  # LinkedIn homepage
    "https://www.netflix.com"  # Netflix homepage
    "https://www.spotify.com"  # Spotify homepage
    "https://www.github.com"  # GitHub homepage

    "https://www.cnn.com"  # CNN news site
    "https://www.bbc.com"  # BBC homepage
    "https://www.nytimes.com"  # The New York Times homepage
    "https://www.forbes.com"  # Forbes homepage
    "https://www.sports.yahoo.com"  # Yahoo Sports homepage
)

SHUFFLED_URLS=($(echo "${URLS[@]}" | tr ' ' '\n' | shuf))
TOTAL_URLS=${#SHUFFLED_URLS[@]}

BATCH_SIZE=10


is_app_installed() {
  local app_name="$1"
  if [ -d "/Applications/${app_name}.app" ] || [ -d "~/Applications/${app_name}.app" ]; then
    return 0
  else
    return 1
  fi
}

# Populate the history of the installed browsers

for browser in "${BROWSERS[@]}"; do
    if is_app_installed $browser; then
        echo "[${browser}]: Installed"

        i=0
        while [ $i -lt $TOTAL_URLS ]; do
            current_batch=("${SHUFFLED_URLS[@]:$i:$BATCH_SIZE}")
            
            for url in "${current_batch[@]}"; do
                osascript -e "tell application \"$browser\" to open location \"$url\""
            done
            
            sleep 10
            osascript -e "tell application \"$browser\" to close every window"

            i=$((i + BATCH_SIZE))
        done
    else
        echo "[${browser}]: Not installed"
    fi
done
