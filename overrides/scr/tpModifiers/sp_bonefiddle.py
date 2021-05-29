from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Bonefiddle"

def bonefiddleSpellBeginRound(attachee, args, evt_obj):
    if args.get_arg(1) >= 0:
        spellDamageDice = dice_new('3d6')
        spellPacket = tpdp.SpellPacket(args.get_arg(0))
        game.create_history_freeform("{} saves versus ~Bonefiddle~[TAG_SPELLS_BONEFIDDLE]\n\n".format(attachee.description))
        if attachee.saving_throw_spell(args.get_arg(2), D20_Save_Fortitude, D20STD_F_NONE, spellPacket.caster, args.get_arg(0)): #save for no damage and to end spell immediately
            attachee.float_text_line("Bonefiddle saved")
            args.set_arg(1, -1)
        else:
            attachee.float_text_line("Bonefiddle damage", tf_red)
            attachee.spell_damage(spellPacket.caster, D20DT_SONIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0)) #is there a way to change unknown to spell name in the history window?
    return 0

def bonefiddleSpellSkillPenalty(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-20, 0, "~Bonefiddle~[TAG_SPELLS_BONEFIDDLE] Penalty") # Bonefiddle gives -20 to Move Silently
    return 0

bonefiddleSpell = PythonModifier("sp-Bonefiddle",3) # spell_id, duration, spellDc
bonefiddleSpell.AddHook(ET_OnBeginRound, EK_NONE, bonefiddleSpellBeginRound, ())
bonefiddleSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_MOVE_SILENTLY, bonefiddleSpellSkillPenalty,())
bonefiddleSpell.AddHook(ET_OnConditionAdd, EK_NONE, spell_utils.addConcentration, ())
bonefiddleSpell.AddHook(ET_OnD20Signal, EK_S_Concentration_Broken, spell_utils.checkRemoveSpell, ())
bonefiddleSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
bonefiddleSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
bonefiddleSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, spell_utils.spellEnd, ())
bonefiddleSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
bonefiddleSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
bonefiddleSpell.AddSpellDispelCheckStandard()
bonefiddleSpell.AddSpellTeleportPrepareStandard()
bonefiddleSpell.AddSpellTeleportReconnectStandard()
bonefiddleSpell.AddSpellCountdownStandardHook()
