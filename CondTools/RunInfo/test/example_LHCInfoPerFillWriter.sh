if [ -f writer_simple_test.db ]; then
    rm -i writer_simple_test.db 
fi
cmsRun LHCInfoPerFillWriter_cfg.py size=5 number=7 db=sqlite:writer_simple_test.db 
conddb --db writer_simple_test.db list LHCInfoPerFillFake