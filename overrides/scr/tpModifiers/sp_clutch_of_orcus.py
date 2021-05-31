from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Clutch of Orcus"

def clutchOfOrcusSpellBeginRound(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if args.get_arg(1) >= 0:
        spellDamageDice = dice_new('1d12')
        if attachee.d20_query('Q_Unconscious'): #no save while unconscious
            attachee.float_text_line("Clutch of Orcus damage", tf_red)
            attachee.spell_damage(spellPacket.caster, D20DT_MAGIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0)) #is there a way to change unknown to spell name in the history window?
        else:
            game.create_history_freeform("{} saves versus ~Clutch of Orcus~[TAG_SPELLS_CLUTCH_OF_ORCUS]\n\n".format(attachee.description))
            if attachee.saving_throw_spell(args.get_arg(2), D20_Save_Fortitude, D20STD_F_NONE, spellPacket.caster, args.get_arg(0)): #save for no damage and to end spell immediately
                attachee.float_text_line("Clutch of Orcus saved")
                attachee.d20_send_signal(S_Killed, 'Paralyzed')
                args.set_arg(1, -1)
            else:
                attachee.float_text_line("Clutch of Orcus damage", tf_red)
                attachee.spell_damage(spellPacket.caster, D20DT_MAGIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0)) #is there a way to change unknown to spell name in the history window?
    return 0

clutchOfOrcusSpell = PythonModifier("sp-Clutch of Orcus", 3) # spell_id, duration, spell_dc
clutchOfOrcusSpell.AddHook(ET_OnBeginRound, EK_NONE, clutchOfOrcusSpellBeginRound, ())
clutchOfOrcusSpell.AddHook(ET_OnConditionAdd, EK_NONE, spell_utils.addConcentration, ())
clutchOfOrcusSpell.AddHook(ET_OnD20Signal, EK_S_Concentration_Broken, spell_utils.checkRemoveSpell, ())
clutchOfOrcusSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
clutchOfOrcusSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
clutchOfOrcusSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
clutchOfOrcusSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
clutchOfOrcusSpell.AddSpellDispelCheckStandard()
clutchOfOrcusSpell.AddSpellTeleportPrepareStandard()
clutchOfOrcusSpell.AddSpellTeleportReconnectStandard()
clutchOfOrcusSpell.AddSpellCountdownStandardHook()
