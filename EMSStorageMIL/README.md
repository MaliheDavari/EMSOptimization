# Microgrid with Battery Storage: Mixed Integer Linear Optimization

**System description:**

A Grid-connected microgrid includes two Distributed generation (DG) units, wind turbine (WT), and photovoltaic (PV) panels as renewable energy resources (RERs), and a battery storage to supply microgrid consumers.

**Objective:**

Minimizing the operation cost including the cost of buying electricity from the main grid and the cost of power production of DGs

**Assumptions:**

1) The predicted tariff of the electricity, output power of RESs, and loads are available.
2) The operating cost of the RESs is zero.
3) The considered powers are the average value in each time slot (1 h) = operating step
4) The time horizon is 24 hours.
5) Consider ramp-up and ramp-down constraints on both DGs

**Decision variables:**
<p><i>P<sub>grid</sub>(t)</i>, <i>P<sub>res</sub>(t,i)</i>, <i>P(t,g)</i>, <i>P<sub>s_disch</sub>(t)</i>, and <i>P<sub>s_ch</sub>(t)</i> &in; <b>R</b><sup>+</sup></p>


**Mathematical formulation:**

**Objective Function**

<p>min cost = &sum;<sub>t</sub> { (<i>P<sub>grid</sub>(t) &middot; &Delta;t</i>) &middot; price<sub>grid</sub> + &sum;<sub>g</sub> (price<sub>p_gen</sub> &middot; P<sub>gen</sub>(t) + price<sub>c,gen</sub>) }</p>


## Constraints

**Power Balance**  <p>&sum;<sub>i</sub> P<sub>res</sub>(t,i) + &sum;<sub>g</sub> P(g,t) + P<sub>grid</sub>(t) + (P<sub>s_disch</sub>(t) - P<sub>s_ch</sub>(t)) = P<sub>load</sub>(t), &forall; t</p>
<p>0 &le; P<sub>grid</sub>(t) &le; P<sub>grid_max</sub>, &forall; t</p>
<p>0 &le; P<sub>gen</sub>(g,t) &le; P<sub>gen_max</sub>(g,t), &forall; t,g</p>
<p>0 &le; P<sub>res</sub>(t,i) &le; P<sub>res_max</sub>(t,i), &forall; t,i</p>


**Round Up and Round Down Powers for Generators**
<p>P<sub>gen</sub>(g,t+1) - P<sub>gen</sub>(g,t) &le; RU<sub>gen</sub>(g), &forall; t,g</p>
<p>P<sub>gen</sub>(g,t-1) - P<sub>gen</sub>(g,t) &le; RD<sub>gen</sub>(g), &forall; t,g</p>



**Battery Storage**
<p>SoC(t) = SoC(t-1) + <sup>&eta;<sub>s_ch</sub></sup>&frasl;<sub>CAP</sub> (P<sub>s_ch</sub>(t) &middot; &Delta;t) - <sup>1</sup>&frasl;<sub>&eta;<sub>s_disch</sub> &middot; CAP</sub> (P<sub>s_disch</sub>(t) &middot; &Delta;t), &forall; t</p>
<p>0 &le; P<sub>s_ch</sub>(t) &le; P<sub>s_ch_max</sub> &times; X<sub>s</sub>(t), &forall; t</p>
<p>0 &le; P<sub>s_disch</sub>(t) &le; P<sub>s_disch_max</sub> &times; (1 - X<sub>s</sub>(t)), &forall; t</p>
<p>SoC<sub>min</sub> &le; SoC(t) &le; SoC<sub>max</sub>, &forall; t</p>
