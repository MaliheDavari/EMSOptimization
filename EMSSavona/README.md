notes:

1) change storage equation eff discharge 1.05 to .95 and go to enominator
2) add to constraints
```
W_s(1,1)=0.5;          %initial state of storage
```
3) if you wanted to write non linear be careful that mass flow rate of nodes and pipes is in one time and not T time intervals
4) I have removed the leakage so there no health index and m_z
5) check pressure equations that affects the flow 
6) change equations related to heat loss in pipes 