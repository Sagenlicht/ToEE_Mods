from toee import *
import tpactions
import tpdp

def GetActionName():
    return "Radial Menu Ray Attack"

def GetActionDefinitionFlags():
    return D20ADF_MagicEffectTargeting | D20ADF_Breaks_Concentration | D20ADF_TriggersCombat | D20ADF_UseCursorForPicking | D20ADF_TriggersAoO #I assume fireing a ray in a later round should also provoke AoO

def GetTargetingClassification():
    return D20TC_SingleExcSelf

def GetActionCostType():
    return D20ACT_Standard_Action

def AddToSequence(d20action, action_seq, tb_status):

    if d20action.performer.d20_query(Q_Prone):
        getupAction = d20action
        getupAction.action_type = D20A_STAND_UP
        action_seq.add_action(getupAction)

    action_seq.add_action(d20action)
    return AEC_OK

def ProjectileHit(d20action, proj, obj2):
    print "Ray Projectile Hit"
    d20action.performer.apply_projectile_hit_particles(proj, d20action.flags)
    return 1