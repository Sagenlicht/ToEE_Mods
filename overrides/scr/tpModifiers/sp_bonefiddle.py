from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Bonefiddle"

def bonefiddleSpellBeginRound(attachee, args, evt_obj):
    if args.get_arg(1) >= 0:
        spellDamageDice = dice_new('3d6')
        #spellId = args.get_arg(0)
        spellPacket = tpdp.SpellPacket(args.get_arg(0))
        game.create_history_freeform(attachee.description + " saves versus ~Bonefiddle~[TAG_SPELLS_BONEFIDDLE]\n\n")
        if attachee.saving_throw_spell(args.get_arg(2), D20_Save_Fortitude, D20STD_F_NONE, spellPacket.caster, args.get_arg(0)): #save for no damage and to end spell immediately
            attachee.float_text_line("Bonefiddle saved")
            args.set_arg(1, -1)
        else:
            attachee.float_text_line("Bonefiddle damage", tf_red)
            attachee.spell_damage(spellPacket.caster, D20DT_SONIC, spellDamageDice, D20DAP_MAGIC, D20A_CAST_SPELL, args.get_arg(0)) #is there a way to change unknown to spell name in the history window?
    return 0
    
def bonefiddleSpellSkillPenalty(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-20, 0, "~Bonefiddle~[TAG_SPELLS_BONEFIDDLE] Penalty") # Bonefiddle gives -20 to Move Silently
    return 0

def bonefiddleSpellAddConcentration(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.caster.condition_add_with_args('sp-Concentrating', args.get_arg(0))
    return 0

def bonefiddleSpellConcentrationBroken(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.spell_enum == 0:
        return 0
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def bonefiddleSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Bonefiddle ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Bonefiddle ({} rounds)".format(args.get_arg(1)))
    return 0

def bonefiddleSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("BONEFIDDLE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("BONEFIDDLE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def bonefiddleSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def bonefiddleSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def bonefiddleSpellSpellEnd(attachee, args, evt_obj):
    print "BonefiddleSpellEnd"
    return 0

bonefiddleSpell = PythonModifier("sp-Bonefiddle",3) # spell_id, duration, spellDc
bonefiddleSpell.AddHook(ET_OnBeginRound, EK_NONE, bonefiddleSpellBeginRound, ())
bonefiddleSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_MOVE_SILENTLY, bonefiddleSpellSkillPenalty,())
bonefiddleSpell.AddHook(ET_OnConditionAdd, EK_NONE, bonefiddleSpellAddConcentration,())
bonefiddleSpell.AddHook(ET_OnD20Signal, EK_S_Concentration_Broken, bonefiddleSpellConcentrationBroken, ())
bonefiddleSpell.AddHook(ET_OnGetTooltip, EK_NONE, bonefiddleSpellTooltip, ())
bonefiddleSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, bonefiddleSpellEffectTooltip, ())
bonefiddleSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, bonefiddleSpellSpellEnd, ())
bonefiddleSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, bonefiddleSpellHasSpellActive, ())
bonefiddleSpell.AddHook(ET_OnD20Signal, EK_S_Killed, bonefiddleSpellKilled, ())
bonefiddleSpell.AddSpellDispelCheckStandard()
bonefiddleSpell.AddSpellTeleportPrepareStandard()
bonefiddleSpell.AddSpellTeleportReconnectStandard()
bonefiddleSpell.AddSpellCountdownStandardHook()
