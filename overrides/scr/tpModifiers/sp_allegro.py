from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Allegro"

def allegroSpellMovementBonus(attachee, args, evt_obj):
    moveSpeedBase = attachee.stat_level_get(stat_movement_speed)
    evt_obj.bonus_list.add(min(moveSpeedBase, 30), 12 ,"~Allegro~[TAG_SPELLS_ALLEGRO] ~Enhancement~[TAG_ENHANCEMENT_BONUS] Bonus") #Allegro adds 30ft. to movement speed, but is capped at double original speed.
    return 0

allegroSpell = PythonModifier("sp-Allegro", 2) # spell_id, duration
allegroSpell.AddHook(ET_OnGetMoveSpeedBase, EK_NONE, allegroSpellMovementBonus,())
allegroSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
allegroSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
allegroSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, spell_utils.spellEnd, ())
allegroSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
allegroSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
allegroSpell.AddSpellDispelCheckStandard()
allegroSpell.AddSpellTeleportPrepareStandard()
allegroSpell.AddSpellTeleportReconnectStandard()
allegroSpell.AddSpellCountdownStandardHook()
