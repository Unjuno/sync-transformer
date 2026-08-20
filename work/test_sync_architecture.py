import numpy as np
from sync_architecture import EpisodicMemory,CausalPrefixIndex,ordered_future_transport,fuse,safety_gate,validate_ranked,hierarchical_select

def test_causal_and_ordered_transport():
    m=EpisodicMemory(); m.add([0,1],[10,11],end_time=1); m.add([0,1],[20,21],end_time=100)
    r=CausalPrefixIndex(m).search([0,1],query_time=50,horizon=2,k=4)
    assert len(r)==1 and np.allclose(ordered_future_transport(r),[[10,11]])

def test_gate_fails_closed():
    d=safety_gate(True,False,True,True,True,1.0)
    assert not d.allowed and d.alpha==0

def test_fusion_preserves_offset_order():
    out=fuse(np.array([0.,0.]),np.array([[2.,4.],[4.,6.]]),alpha=.5)
    assert np.allclose(out,[1.5,2.5])

def test_ranked_contract_rejects_future_leakage():
    m=EpisodicMemory(); m.add([0,1],[2,3],end_time=9)
    r=[(0.0,m._episodes[0])]
    try: validate_ranked(r,query_time=10,horizon=2,prefix_len=2)
    except ValueError as e: assert 'future leakage' in str(e)
    else: raise AssertionError('leakage was not rejected')

def test_hierarchical_selection_contract():
    m=EpisodicMemory()
    for i in range(20): m.add(np.ones(3)*i,np.ones(2)*i,i,True)
    r=hierarchical_select(CausalPrefixIndex(m),np.zeros(3),100,2,coarse_k=12,final_k=4)
    assert len(r)==4
