#!/bin/bash
# Setup iMac auto power: wake 6am + shutdown midnight, DAILY
# Run ONCE with sudo:  sudo ~/ai-agent-hermes-vn/setup_power_schedule.sh
# macOS 12 pmset format: "MM/DD/YYYY HH:MM:SS" (no native repeat) -> we arm 7 days ahead.

echo "=== Current schedule ==="
pmset -g sched

echo "=== Cancel old ==="
pmset schedule cancel 2>/dev/null

echo "=== Arming next 7 days (wake 06:00, shutdown 00:00) ==="
for i in $(seq 0 6); do
  D=$(date -v+${i}d +"%m/%d/%Y")
  pmset schedule wakeorpoweron "${D} 06:00:00" 2>&1
  pmset schedule shutdown      "${D} 00:00:00" 2>&1
done

echo ""
echo "=== New schedule (next 7 days) ==="
pmset -g sched
echo ""
echo "✅ Done. Re-run this script weekly to keep it armed, or I'll add a LaunchDaemon to auto-rearm."
