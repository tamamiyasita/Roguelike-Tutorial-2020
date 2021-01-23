from actor.items.cirsium import Cirsium
from actor.skills.leaf_blade import LeafBlade
from actor.items.ebony import Ebony
from actor.skills.branch_baton import BranchBaton
from actor.items.paeonia import Paeonia
from actor.skills.healing import Healing
from actor.skills.seed_shot import SeedShot

from actor.states.poison_status import PoisonStatus

skill_lists =[
            Cirsium(),
            Ebony(),
            Paeonia(),
            LeafBlade(),
            BranchBaton(),
            Healing(),
            SeedShot()
            ]

skill_dict = {skill.name:skill for skill in skill_lists}

PoisonStatus()