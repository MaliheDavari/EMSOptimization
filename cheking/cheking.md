Decision variables:

<p><i>P<sub>grid</sub>(t)</i>, <i>P<sub>res</sub>(t,i)</i>, and <i>P(t,g)</i> &isin; <b>R</b><sup>+</sup></p>



Objective Function

<p>min cost = &sum;<sub>t</sub> { (<i>P<sub>grid</sub>(t) &middot; &Delta;t</i>) &middot; price<sub>grid</sub> + &sum;<sub>g</sub> (price<sub>p_gen</sub> &middot; P<sub>gen</sub>(t) + price<sub>c,gen</sub>) }</p>

Power Balance

<p>&sum;<sub>i</sub> P<sub>res</sub>(t,i) + &sum;<sub>g</sub> P(g,t) + P<sub>grid</sub>(t) = P<sub>load</sub>(t), &forall; t</p>
<p>0 &le; P<sub>grid</sub>(t) &le; P<sub>grid_max</sub>, &forall; t</p>
<p>0 &le; P<sub>gen</sub>(g,t) &le; P<sub>gen_max</sub>(g,t), &forall; t,g</p>
<p>0 &le; P<sub>res</sub>(t,i) &le; P<sub>res_max</sub>(t,i), &forall; t,i</p>

Round Up and Round Down Powers for Generators:

<p>P<sub>gen</sub>(g,t+1) - P<sub>gen</sub>(g,t) &le; RU<sub>gen</sub>(g), &forall; t,g</p>
<p>P<sub>gen</sub>(g,t-1) - P<sub>gen</sub>(g,t) &le; RD<sub>gen</sub>(g), &forall; t,g</p>