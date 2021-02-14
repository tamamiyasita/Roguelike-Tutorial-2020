from actor.items.silver_grass import SilverGrass
from actor.items.ebony import Ebony
from actor.items.paeonia import Paeonia
from actor.items.pineapple import Pineapple
from actor.items.sunflower import Sunflower

from actor.skills.branch_baton import BranchBaton
from actor.skills.grass_cutter import GrassCutter
from actor.skills.healing import Healing
from actor.skills.seed_shot import SeedShot
from actor.skills.p_grenade import P_Grenade
from actor.skills.poison_dart import PoisonDart

from actor.states.poison_status import PoisonStatus

skill_lists =[
            SilverGrass(),
            Ebony(),
            Paeonia(),
            Sunflower(),
            Pineapple(),

            GrassCutter(),
            BranchBaton(),
            Healing(),
            SeedShot(),
            P_Grenade(),
            PoisonDart()
        

            ]

skill_dict = {skill.name:skill for skill in skill_lists}

# PoisonStatus()