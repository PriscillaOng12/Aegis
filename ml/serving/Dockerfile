FROM pytorch/torchserve:0.8.2-cpu

# Copy model artefacts
COPY models /home/model-server/model_store/
COPY handler.py /home/model-server/
COPY config.properties /home/model-server/

RUN torch-model-archiver --model-name aegis_model \
    --version 1.0 \
    --handler handler.py \
    --extra-files /home/model-server/model_store/shap_background.json \
    --serialized-file /home/model-server/model_store/xgboost_model.json \
    --export-path /home/model-server/model_store

CMD ["torchserve", "--start", "--model-store", "/home/model-server/model_store", "--models", "aegis_model=aegis_model.mar", "--ts-config", "/home/model-server/config.properties"]