"""nav17 — open-data engine for the Nav1.7 genetic-pharmacological asymmetry analysis."""
from .substitution import (
    NAV, SUBSTITUTORS, KCNQ, TARGET,
    substitution_capacity, asymmetry_verdict,
)
from .homeostat import (
    U_MAX, ANALGESIA_MIN, AUTO_MAX,
    deficit, deficit_ss, gn_crit, d1_decision,
)
__version__ = "0.1.0"
