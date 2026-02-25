# ...existing code...

if __name__ == "__main__":
    # ...existing code...
    
    with mlflow.start_run() as run:
        # ...training code...
        mlflow.xgboost.log_model(xgb_model, artifact_path="model")
        
        # ✅ DEBUG - print the actual run_id
        run_id = run.info.run_id
        print(f"\n[DEBUG] run_id: {run_id}")
        print(f"[DEBUG] run_id length: {len(run_id)}")
        print(f"[DEBUG] run_id type: {type(run_id)}")
        
        # Store to SSM
        ssm.put_parameter(
            Name="/emotion_analysis/mlflow/run_id",
            Value=run_id,
            Overwrite=True,
            Type="String"
        )
        
        # ✅ VERIFY - read it back immediately
        verify_param = ssm.get_parameter(Name="/emotion_analysis/mlflow/run_id")
        stored_run_id = verify_param['Parameter']['Value']
        print(f"[DEBUG] Verified stored run_id: {stored_run_id}")
        
        if stored_run_id.startswith("m-"):
            print(f"[ERROR] WRONG! Stored model ID instead of run ID!")
        elif stored_run_id == run_id:
            print(f"[SUCCESS] Stored run_id correctly")
# ...existing code...