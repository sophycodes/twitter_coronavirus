#!/bin/bash

# Create logs directory if it doesn't exist
mkdir -p logs

# Loop over all 2020 Twitter data files
for file in /data/Twitter\ dataset/geoTwitter20*.zip; do
    echo "Starting map.py for $file"
    
    # Run map.py in background with nohup
    nohup python src/map.py \
        --input_path "$file" \
        --output_folder outputs \
        > "logs/$(basename "$file").log" 2>&1 &
done

echo "All map.py jobs started in background"
echo "Check progress with: tail -f logs/*.log"
echo "Check running jobs with: ps aux | grep map.py"
