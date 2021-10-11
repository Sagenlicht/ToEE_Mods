from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Veil of Shadow"

def veilOfShadowSpellConcealment(attachee, args, evt_obj):
    bonusValue = 20 #Veil of Shadow grants 20% Concealment
    bonusType = 19 #ID 13 = Concealment
    evt_obj.bonus_list.add(bonusValue, bonusType, "~Veil of Shadow~[TAG_SPELLS_VEIL_OF_SHADOW] Concealment Bonus")
    return 0

def veilOfShadowSpellCheckDispelCondition(attachee, args, evt_obj):
    #Veil of Shadow is dispelled by daylight
    if game.is_outdoor() and game.is_daytime():
        attachee.float_text_line("Dispelled by daylight")
        args.set_arg(1, -1)
    return 0

veilOfShadowSpell = PythonModifier("sp-Veil of Shadow", 3, False) # spell_id, duration, empty
veilOfShadowSpell.AddHook(ET_OnBeginRound, EK_NONE, veilOfShadowSpellCheckDispelCondition,())
veilOfShadowSpell.AddHook(ET_OnGetDefenderConcealmentMissChance, EK_NONE, veilOfShadowSpellConcealment,())
veilOfShadowSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
veilOfShadowSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
veilOfShadowSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
veilOfShadowSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
veilOfShadowSpell.AddSpellDispelCheckStandard()
veilOfShadowSpell.AddSpellTeleportPrepareStandard()
veilOfShadowSpell.AddSpellTeleportReconnectStandard()
veilOfShadowSpell.AddSpellCountdownStandardHook()
