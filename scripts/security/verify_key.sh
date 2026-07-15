#!/bin/bash
# verify_key.sh — 密钥有效性验证，不把明文暴露给 Hermes 的对话上下文
#
# 用法：
#   ./verify_key.sh fred
#   ./verify_key.sh exchangerate
#   ./verify_key.sh tavily
#
# Hermes 只被允许调用这个脚本、读它的退出码和 stdout 里的 "OK"/"FAIL"，
# 不允许直接 cat .env 或在对话里打印 key 的值来做验证。

set -euo pipefail

if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

check_http_code() {
  local expected="$1"
  local actual="$2"
  if [ "$actual" == "$expected" ]; then
    echo "OK"
  else
    echo "FAIL (http_code=$actual)"
    exit 1
  fi
}

case "$1" in
  fred)
    code=$(curl -s -o /dev/null -w "%{http_code}" \
      "https://api.stlouisfed.org/fred/series?series_id=GNPCA&api_key=${FRED_API_KEY}&file_type=json")
    check_http_code "200" "$code"
    ;;
  exchangerate)
    code=$(curl -s -o /dev/null -w "%{http_code}" \
      "https://v6.exchangerate-api.com/v6/${EXCHANGERATE_API_KEY}/latest/USD")
    check_http_code "200" "$code"
    ;;
  tavily)
    code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "https://api.tavily.com/search" \
      -H "Content-Type: application/json" \
      -d "{\"api_key\": \"${TAVILY_API_KEY}\", \"query\": \"test\"}")
    check_http_code "200" "$code"
    ;;
  reddit)
    code=$(curl -s -o /dev/null -w "%{http_code}" \
      -H "Authorization: Bearer ${REDDIT_ACCESS_TOKEN}" \
      "https://oauth.reddit.com/api/v1/me")
    check_http_code "200" "$code"
    ;;
  *)
    echo "未知的 key 名称: $1"
    echo "支持: fred / exchangerate / tavily / reddit"
    exit 2
    ;;
esac
