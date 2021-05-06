from actor.actor import Actor

from actor.characters.PC import Player
from actor.characters.orcs import Orc, Troll
from actor.characters.crab import Crab
from actor.characters.rat import Water_vole
from actor.characters.npc import Villager, Citizen


from actor.items.silver_grass import SilverGrass
from actor.items.ebony import Ebony
from actor.items.paeonia import Paeonia
from actor.items.sunflower import Sunflower
from actor.items.pineapple import Pineapple
from actor.items.aconite import Aconite
from actor.items.banana_flower import Bananaflower
from actor.items.bamboo_flower import Bambooflower


from actor.skills.grass_cutter import GrassCutter
from actor.skills.branch_baton import BranchBaton
from actor.skills.healing import Healing
from actor.skills.seed_shot import SeedShot
from actor.skills.p_grenade import P_Grenade
from actor.skills.poison_dart import PoisonDart
from actor.skills.bamboo_blade import BambooBlade

from actor.states.poison_status import PoisonStatus

from actor.map_obj.wall import Wall
from actor.map_obj.floor import Floor
from actor.map_obj.stairs import Up_Stairs, Down_Stairs
from actor.map_obj.door import DoorW, DoorH


def restore_actor(actor_dict):
    actor_name = list(actor_dict.keys())[0]

    if actor_name == "Actor":
        actor = Actor()
    elif actor_name == "Player":
        actor = Player()


    elif actor_name == "SilverGrass":
        actor = SilverGrass()
    elif actor_name == "Ebony":
        actor = Ebony()
    elif actor_name == "Paeonia":
        actor = Paeonia()
    elif actor_name == "Sunflower":
        actor = Sunflower()
    elif actor_name == "Pineapple":
        actor = Pineapple()
    elif actor_name == "Aconite":
        actor = Aconite()
    elif actor_name == "Bananaflower":
        actor = Bananaflower()
    elif actor_name == "Bambooflower":
        actor = Bambooflower()
    

    elif actor_name == "GrassCutter":
        actor = GrassCutter()
    elif actor_name == "BranchBaton":
        actor = BranchBaton()
    elif actor_name == "Healing":
        actor = Healing()
    elif actor_name == "SeedShot":
        actor = SeedShot()
    elif actor_name == "p_grenade":
        actor = P_Grenade()
    elif actor_name == "PoisonDart":
        actor = PoisonDart()
    elif actor_name == "BambooBlade":
        actor = BambooBlade()


    elif actor_name == "PoisonStatus":
        actor = PoisonStatus()

    elif actor_name == "Orc":
        actor = Orc()
    elif actor_name == "Troll":
        actor = Troll()
    elif actor_name == "Crab":
        actor = Crab()
    elif actor_name == "Water_vole":
        actor = Water_vole()
    elif actor_name == "Citizen":
        actor = Citizen()
    elif actor_name == "Villager":
        actor = Villager()



    elif actor_name == "Wall":
        actor = Wall()
    elif actor_name == "Floor":
        actor = Floor()
    elif actor_name == "Up_Stairs":
        actor = Up_Stairs()
    elif actor_name == "Down_Stairs":
        actor = Down_Stairs()
    elif actor_name == "DoorH":
        actor = DoorH()
    elif actor_name == "DoorW":
        actor = DoorW()
    else:
        raise ValueError(f"Error, don't know how to restore {actor_name}.")

    actor.restore_from_dict(actor_dict[actor_name])

    return actor
