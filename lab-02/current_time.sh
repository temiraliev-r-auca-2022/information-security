#!/bin/bash

current_hour=$(date +%H)
current_minute=$(date +%M)

end_hour=18
end_minute=0

remaining_minutes=$(( (end_hour*60 + end_minute) - (current_hour*60 + current_minute) ))

hours_left=$(( remaining_minutes / 60 ))
minutes_left=$(( remaining_minutes % 60 ))

echo "Current time: $(date +%H:%M)"
echo "Work day ends after $hours_left hours and $minutes_left minutes."
