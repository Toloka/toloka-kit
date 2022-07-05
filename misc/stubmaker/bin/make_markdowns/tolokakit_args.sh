cat << EOF
--module-root toloka \
--src-root $(dirname $0)/../../../../docs/reference \
--output-dir $(dirname $0)/../../../../docs/reference
--described-objects $(dirname $0)/../../described_objects_tolokakit.py
--github-source-url https://github.com/Toloka/toloka-kit/blob/v0.1.26/src
EOF
