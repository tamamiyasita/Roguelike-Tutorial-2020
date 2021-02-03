from actor.items.cirsium import Cirsium
from actor.items.ebony import Ebony
from actor.items.paeonia import Paeonia
from actor.items.pineapple import Pineapple
from actor.items.sunflower import Sunflower

from actor.skills.branch_baton import BranchBaton
from actor.skills.leaf_blade import LeafBlade
from actor.skills.healing import Healing
from actor.skills.seed_shot import SeedShot
from actor.skills.p_grenade import P_Grenade

from actor.states.poison_status import PoisonStatus

skill_lists =[
            Cirsium(),
            Ebony(),
            Paeonia(),
            Sunflower(),
            Pineapple(),

            LeafBlade(),
            BranchBaton(),
            Healing(),
            SeedShot(),
            P_Grenade()
        

            ]

skill_dict = {skill.name:skill for skill in skill_lists}

PoisonStatus()