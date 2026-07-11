if [ -f writer_simple_test.db ]; then
    rm -i writer_simple_test.db 
fi
cmsRun ${CMSSW_BASE}/src/CondTools/RunInfo/test/LHCInfoPerFillWriter_cfg.py size=50 number=7 db=sqlite:writer_simple_test.db 
conddb --db writer_simple_test.db list LHCInfoPerFillFake
