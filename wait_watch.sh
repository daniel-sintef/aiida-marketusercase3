JOB_UUID=$(cat JOB_UUID)
WORKDIR=/tmp/${JOB_UUID}
mkdir -p $WORKDIR

INPUT_FILE=./inputs.json
cp $INPUT_FILE $WORKDIR/

OUTPUT_FILE=${WORKDIR}/test
while true
do
    if [ -e "$OUTPUT_FILE" ]; then
       echo "$OUTPUT_FILE exists."
       break
    fi	
done


