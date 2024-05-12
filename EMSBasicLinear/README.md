# Basic Microgrid: Linear Optimization

**System description:**

A Grid-connected microgrid includes two Distributed generation (DG) units, wind turbine (WT), and photovoltaic (PV) panels as renewable energy resources (RERs), to supply microgrid consumers.

**Objective:**

Minimizing the operation cost including the cost of buying electricity from the main grid and the cost of power production of DGs

**Assumptions:**

1) The predicted tariff of the electricity, output power of RESs, and loads are available.
2) The operating cost of the RESs is zero.
3) The considered powers are the average value in each time slot (1 h) = operating step
4) The time horizon is 24 hours.
5) Consider ramp-up and ramp-down constraints on both DGs

**Decision variables:**
$$P_{\text{grid}}(t), \quad P_{\text{res}}(t,i), \quad \text{and} \quad P(t,g) \in \mathbb{R}^{+}$$


**Mathematical formulation:**

**Objective Function**
$$\min \text{ cost} = \sum_{t} \left( (P_{\text{grid}}(t) \cdot \Delta t) \cdot price_{\text{\_grid}} + \sum_{g} (price_{p_gen} \cdot P_{gen}(t) + price_{c,gen}) \right)$$

## Constraints

**Power Balance**   $$\sum_{i} P_{\text{res}}(t,i) + \sum_{g} P(g,t) + P_{\text{grid}}(t) = P_{\text{load}}(t), \quad \forall t$$

$$0 \leq P_{\text{grid}}(t) \leq P_{\text{grid\_max}}, \quad \forall t$$


$$0 \leq P_{\text{gen}}(g,t) \leq P_{\text{gen\_max}}(g,t), \quad \forall t,g$$
$$0 \leq P_{\text{res}}(t,i) \leq P_{\text{res\_max}}(t,i), \quad \forall t,i$$

**Round Up and Round Down Powers for Generators:**
$$P_{\text{gen}}(g,t+1) - P{\text{gen}}(g,t) \leq RU_{\text{gen}}(g), \quad \forall t,g$$
$$P_{\text{gen}}(g,t-1) - P{\text{gen}}(g,t) \leq RD_{\text{gen}}(g), \quad \forall t,g$$

